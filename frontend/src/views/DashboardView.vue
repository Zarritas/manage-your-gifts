<template>
  <div>
    <nav class="navbar">
      <router-link to="/dashboard" class="navbar-brand">🎁 {{ t('app.name') }}</router-link>
      <div class="navbar-actions">
        <router-link to="/settings" class="btn btn-ghost">⚙️</router-link>
        <button class="btn btn-ghost" @click="authStore.logout">{{ t('auth.logout') }}</button>
      </div>
    </nav>
    
    <div class="page container">
      <div class="page-header">
        <h1 class="page-title">{{ t('dashboard.title') }}</h1>
        <router-link to="/groups/new" class="btn btn-primary">
          + {{ t('dashboard.createGroup') }}
        </router-link>
      </div>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>
      
      <template v-else>
        <!-- Active Groups -->
        <section v-if="activeGroups.length > 0">
          <h2 style="margin-bottom: 16px; color: var(--text-secondary); font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">
            {{ t('dashboard.activeGroups') }}
          </h2>
          <div class="group-grid">
            <router-link
              v-for="group in activeGroups"
              :key="group.id"
              :to="`/groups/${group.id}`"
              class="card group-card"
            >
              <div class="group-card-name">{{ group.name }}</div>
              <div class="group-card-desc">{{ group.description || '' }}</div>
              <div class="group-card-meta">
                <span>👥 {{ group.member_count }} {{ t('dashboard.members') }}</span>
                <span v-if="group.is_admin" class="badge badge-info">Admin</span>
              </div>
            </router-link>
          </div>
        </section>
        
        <!-- Closed Groups -->
        <section v-if="closedGroups.length > 0" style="margin-top: 32px;">
          <h2 style="margin-bottom: 16px; color: var(--text-secondary); font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">
            {{ t('dashboard.closedGroups') }}
          </h2>
          <div class="group-grid">
            <router-link
              v-for="group in closedGroups"
              :key="group.id"
              :to="`/groups/${group.id}`"
              class="card group-card"
              style="opacity: 0.7;"
            >
              <div style="display: flex; justify-content: space-between; align-items: start;">
                <div class="group-card-name">{{ group.name }}</div>
                <span class="badge badge-warning">{{ t('groups.closed') }}</span>
              </div>
              <div class="group-card-desc">{{ group.description || '' }}</div>
              <div class="group-card-meta">
                <span>👥 {{ group.member_count }} {{ t('dashboard.members') }}</span>
              </div>
            </router-link>
          </div>
        </section>
        
        <!-- Empty State -->
        <div v-if="activeGroups.length === 0 && closedGroups.length === 0" class="empty-state">
          <div class="empty-state-icon">📭</div>
          <h3 class="empty-state-title">{{ t('dashboard.noGroups') }}</h3>
          <router-link to="/groups/new" class="btn btn-primary">
            + {{ t('dashboard.createGroup') }}
          </router-link>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useSocketStore } from '@/stores/socket'
import { groupsApi, type Group } from '@/api'

const { t } = useI18n()
const authStore = useAuthStore()
const socketStore = useSocketStore()

const groups = ref<Group[]>([])
const loading = ref(true)

const activeGroups = computed(() => groups.value.filter(g => g.status === 'active'))
const closedGroups = computed(() => groups.value.filter(g => g.status === 'closed'))

const loadGroups = async (showLoading = true) => {
  if (showLoading) loading.value = true
  try {
    groups.value = await groupsApi.list()
  } catch (e) {
    console.error('Failed to load groups:', e)
  } finally {
    if (showLoading) loading.value = false
  }
}

const handleSocketMessage = (data: any) => {
  // If we are added to or removed from a group, reload the list
  if (data.type === 'MEMBER_UPDATE') {
    if ((data.action === 'accepted' || data.action === 'removed') && data.user_id === authStore.user?.id) {
       console.log('Reloading groups due to socket update:', data)
       loadGroups(false)
    }
  }
}

onMounted(() => {
  loadGroups()
  socketStore.onMessage(handleSocketMessage)
})

onUnmounted(() => {
  socketStore.removeListener(handleSocketMessage)
})
</script>
