<template>
  <div>
    <nav class="navbar">
      <router-link to="/dashboard" class="navbar-brand">🎁 {{ t('app.name') }}</router-link>
      <div class="navbar-actions">
        <router-link to="/settings" class="btn btn-ghost">⚙️</router-link>
      </div>
    </nav>
    
    <div class="page container">
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>
      
      <template v-else-if="group">
        <!-- Header -->
        <div class="page-header">
          <div>
            <h1 class="page-title">{{ group.name }}</h1>
            <p v-if="group.description" style="color: var(--text-secondary); margin-top: 4px;">
              {{ group.description }}
            </p>
          </div>
          <div style="display: flex; gap: 8px;">
            <router-link v-if="group.status === 'active'" :to="`/groups/${group.id}/gifts/new`" class="btn btn-primary">
              + {{ t('gifts.addGift') }}
            </router-link>
          </div>
        </div>
        
        <!-- Closed Warning -->
        <div v-if="group.status === 'closed'" class="alert alert-warning">
          {{ t('groups.closedMessage') }}
        </div>
        
        <!-- Tabs -->
        <div class="tabs">
          <button 
            class="tab" 
            :class="{ active: activeTab === 'gifts' }"
            @click="activeTab = 'gifts'"
          >
            🎁 {{ t('gifts.title') }}
          </button>
          <button 
            class="tab" 
            :class="{ active: activeTab === 'members' }"
            @click="activeTab = 'members'"
          >
            👥 {{ t('groups.members') }}
          </button>
          <button 
            v-if="group.is_admin && group.status === 'active'"
            class="tab" 
            :class="{ active: activeTab === 'invite' }"
            @click="activeTab = 'invite'"
          >
            ✉️ {{ t('groups.invite') }}
          </button>
          <button 
            v-if="group.is_admin && group.status === 'active'"
            class="tab" 
            :class="{ active: activeTab === 'settings' }"
            @click="activeTab = 'settings'"
          >
            ⚙️ {{ t('settings.title') }}
          </button>
        </div>
        
        <!-- Gifts Tab -->
        <div v-if="activeTab === 'gifts'">
          <div v-if="gifts.length === 0" class="empty-state">
            <div class="empty-state-icon">🎁</div>
            <h3 class="empty-state-title">No gifts yet</h3>
            <router-link v-if="group.status === 'active'" :to="`/groups/${group.id}/gifts/new`" class="btn btn-primary">
              + {{ t('gifts.addGift') }}
            </router-link>
          </div>
          
          <div v-else class="gift-grid">
            <GiftCard 
              v-for="gift in gifts" 
              :key="gift.id" 
              :gift="gift"
              :group-status="group.status"
              @reserve="handleReserve(gift.id)"
              @unreserve="handleUnreserve(gift.id)"
              @mark-purchased="handleMarkPurchased(gift.id)"
              @delete="handleDelete(gift.id)"
            />
          </div>
        </div>
        
        <!-- Members Tab -->
        <div v-if="activeTab === 'members'">
          <!-- Pending Requests (Admin Only) -->
          <div v-if="group.is_admin && pendingMembers.length > 0" style="margin-bottom: 24px;">
            <h3 style="font-size: 14px; color: var(--text-secondary); margin-bottom: 12px; text-transform: uppercase;">
              {{ t('groups.pendingRequests') }} ({{ pendingMembers.length }})
            </h3>
            <div class="member-list">
              <div v-for="member in pendingMembers" :key="member.id" class="member-item">
                <div class="member-info">
                  <div class="member-avatar">{{ member.email[0].toUpperCase() }}</div>
                  <span class="member-email">{{ member.email }}</span>
                  <span class="badge badge-warning">Pending</span>
                </div>
                <div class="member-actions">
                  <button class="btn btn-success btn-sm" @click="acceptMember(member.user_id)">
                    {{ t('groups.accept') }}
                  </button>
                  <button class="btn btn-danger btn-sm" @click="rejectMember(member.user_id)">
                    {{ t('groups.reject') }}
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Accepted Members -->
          <h3 style="font-size: 14px; color: var(--text-secondary); margin-bottom: 12px; text-transform: uppercase;">
            {{ t('groups.members') }} ({{ acceptedMembers.length }})
          </h3>
          <div class="member-list">
            <div v-for="member in acceptedMembers" :key="member.id" class="member-item">
              <div class="member-info">
                <div class="member-avatar">{{ member.email[0].toUpperCase() }}</div>
                <span class="member-email">{{ member.email }}</span>
                <span v-if="member.is_admin" class="badge badge-info">Admin</span>
              </div>
              <div v-if="group.is_admin && !member.is_admin && group.status === 'active'" class="member-actions">
                <button class="btn btn-danger btn-sm" @click="removeMember(member.user_id)">
                  {{ t('groups.remove') }}
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Invite Tab -->
        <div v-if="activeTab === 'invite'">
          <InviteShare :group-id="group.id" />
        </div>
        
        <!-- Settings Tab (Admin) -->
        <div v-if="activeTab === 'settings' && group.is_admin">
          <div class="card" style="max-width: 400px;">
            <h3 style="margin-bottom: 16px;">Danger Zone</h3>
            <button class="btn btn-danger btn-block" @click="handleCloseGroup">
              {{ t('groups.close') }}
            </button>
            <p style="font-size: 12px; color: var(--text-muted); margin-top: 8px;">
              Closing a group makes it read-only. No more changes will be allowed.
            </p>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { groupsApi, giftsApi, type GroupDetail, type Gift } from '@/api'
import { useSocketStore } from '@/stores/socket'
import GiftCard from '@/components/GiftCard.vue'
import InviteShare from '@/components/InviteShare.vue'

const { t } = useI18n()
const route = useRoute()
const socketStore = useSocketStore()

const group = ref<GroupDetail | null>(null)
const gifts = ref<Gift[]>([])
const loading = ref(true)
const activeTab = ref<'gifts' | 'members' | 'invite' | 'settings'>('gifts')

const pendingMembers = computed(() => group.value?.members.filter(m => m.status === 'pending') || [])
const acceptedMembers = computed(() => group.value?.members.filter(m => m.status === 'accepted') || [])

// Socket handler
const handleSocketMessage = (data: any) => {
  if (data.group_id === group.value?.id) {
    if (['GIFT_UPDATE', 'MEMBER_UPDATE'].includes(data.type)) {
      loadData(false) // Reload data silently
    }
  }
}

async function loadData(showLoading = true) {
  const groupId = route.params.id as string
  if (showLoading) loading.value = true
  
  try {
    const [groupData, giftsData] = await Promise.all([
      groupsApi.get(groupId),
      giftsApi.list(groupId)
    ])
    group.value = groupData
    gifts.value = giftsData
  } catch (e) {
    console.error('Failed to load group:', e)
  } finally {
    if (showLoading) loading.value = false
  }
}

// Member Actions
async function acceptMember(userId: string) {
  if (!group.value) return
  try {
    await groupsApi.acceptMember(group.value.id, userId)
    loadData(false)
  } catch (e) {
    console.error('Failed to accept member:', e)
  }
}

async function rejectMember(userId: string) {
  if (!group.value) return
  try {
    await groupsApi.rejectMember(group.value.id, userId)
    loadData(false)
  } catch (e) {
    console.error('Failed to reject member:', e)
  }
}

async function removeMember(userId: string) {
  if (!group.value || !confirm('Are you sure you want to remove this member?')) return
  try {
    await groupsApi.removeMember(group.value.id, userId)
    loadData(false)
  } catch (e) {
    console.error('Failed to remove member:', e)
  }
}

// Gift Actions
async function handleReserve(giftId: string) {
  try {
    await giftsApi.reserve(giftId)
    loadData(false)
  } catch (e) {
    console.error('Failed to reserve gift:', e)
  }
}

async function handleUnreserve(giftId: string) {
  try {
    await giftsApi.unreserve(giftId)
    loadData(false)
  } catch (e) {
    console.error('Failed to unreserve gift:', e)
  }
}

async function handleMarkPurchased(giftId: string) {
  try {
    await giftsApi.markPurchased(giftId)
    loadData(false)
  } catch (e) {
    console.error('Failed to mark gift as purchased:', e)
  }
}

async function handleDelete(giftId: string) {
  if (!group.value || !confirm('Are you sure you want to delete this gift?')) return
  try {
    await giftsApi.delete(group.value.id, giftId)
    loadData(false)
  } catch (e) {
    console.error('Failed to delete gift:', e)
  }
}

// Group Actions
async function handleCloseGroup() {
  if (!group.value || !confirm('Are you sure you want to close this group? It will become read-only.')) return
  try {
    await groupsApi.close(group.value.id)
    loadData(false)
  } catch (e) {
    console.error('Failed to close group:', e)
  }
}

onMounted(() => {
  loadData()
  socketStore.onMessage(handleSocketMessage)
})

onUnmounted(() => {
  socketStore.removeListener(handleSocketMessage)
})
</script>
