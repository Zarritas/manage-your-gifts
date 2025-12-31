<template>
  <div class="login-container">
    <div class="card login-card card-glass" style="text-align: center;">
      <div class="login-logo">🎁</div>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>
      
      <template v-else-if="success">
        <h2 style="margin-bottom: 8px;">{{ t('groups.join') }}</h2>
        <p class="alert alert-success">{{ t('groups.requestSent') }}</p>
        <router-link to="/dashboard" class="btn btn-primary">
          {{ t('common.back') }}
        </router-link>
      </template>
      
      <template v-else-if="error">
        <div class="alert alert-error">{{ error }}</div>
        <router-link to="/dashboard" class="btn btn-secondary">
          {{ t('common.back') }}
        </router-link>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { groupsApi } from '@/api'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

const loading = ref(true)
const success = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  const groupId = route.params.id as string
  
  try {
    const response = await groupsApi.join(groupId)
    
    if (response.message === 'Already a member') {
      // Redirect to group
      router.push(`/groups/${groupId}`)
    } else {
      success.value = true
    }
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>
