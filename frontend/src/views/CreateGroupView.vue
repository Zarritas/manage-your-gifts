<template>
  <div>
    <nav class="navbar">
      <router-link to="/dashboard" class="navbar-brand">🎁 {{ t('app.name') }}</router-link>
      <div class="navbar-actions">
        <router-link to="/settings" class="btn btn-ghost">⚙️</router-link>
      </div>
    </nav>
    
    <div class="page container container-sm">
      <div class="page-header">
        <h1 class="page-title">{{ t('groups.create') }}</h1>
      </div>
      
      <form class="card" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label class="form-label">{{ t('groups.name') }}</label>
          <input
            v-model="name"
            type="text"
            class="form-input"
            :placeholder="t('groups.namePlaceholder')"
            required
            autofocus
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">{{ t('groups.description') }}</label>
          <textarea
            v-model="description"
            class="form-input"
            :placeholder="t('groups.descriptionPlaceholder')"
            rows="3"
          ></textarea>
        </div>
        
        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>
        
        <div style="display: flex; gap: 12px; margin-top: 24px;">
          <router-link to="/dashboard" class="btn btn-secondary" style="flex: 1;">
            {{ t('common.cancel') }}
          </router-link>
          <button type="submit" class="btn btn-primary" style="flex: 1;" :disabled="loading">
            {{ loading ? t('common.loading') : t('groups.create') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { groupsApi } from '@/api'

const { t } = useI18n()
const router = useRouter()

const name = ref('')
const description = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

async function handleSubmit() {
  loading.value = true
  error.value = null
  
  try {
    const group = await groupsApi.create(name.value, description.value || undefined)
    router.push(`/groups/${group.id}`)
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>
