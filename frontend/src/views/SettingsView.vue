<template>
  <div>
    <nav class="navbar">
      <router-link to="/dashboard" class="navbar-brand">🎁 {{ t('app.name') }}</router-link>
    </nav>
    
    <div class="page container container-sm">
      <div class="page-header">
        <h1 class="page-title">{{ t('settings.title') }}</h1>
      </div>
      
      <!-- Language -->
      <div class="card" style="margin-bottom: 24px;">
        <h3 style="margin-bottom: 16px;">{{ t('settings.language') }}</h3>
        <div style="display: flex; gap: 12px;">
          <button 
            class="btn" 
            :class="locale === 'en' ? 'btn-primary' : 'btn-secondary'"
            @click="changeLanguage('en')"
          >
            🇬🇧 English
          </button>
          <button 
            class="btn" 
            :class="locale === 'es' ? 'btn-primary' : 'btn-secondary'"
            @click="changeLanguage('es')"
          >
            🇪🇸 Español
          </button>
        </div>
      </div>
      
      <!-- Search Stores -->
      <div class="card">
        <h3 style="margin-bottom: 16px;">{{ t('settings.searchStores') }}</h3>
        
        <div class="member-list" style="margin-bottom: 16px;">
          <div v-for="(store, index) in stores" :key="index" class="member-item">
            <div class="member-info">
              <span>{{ store.name }}</span>
            </div>
            <button class="btn btn-danger btn-sm" @click="removeStore(index)">×</button>
          </div>
        </div>
        
        <div v-if="showAddStore" style="margin-bottom: 16px;">
          <div class="form-group">
            <label class="form-label">{{ t('settings.storeName') }}</label>
            <input v-model="newStoreName" type="text" class="form-input" placeholder="Amazon" />
          </div>
          <div class="form-group">
            <label class="form-label">{{ t('settings.storeUrl') }}</label>
            <input v-model="newStoreUrl" type="text" class="form-input" placeholder="https://amazon.com/s?k={query}" />
          </div>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-secondary" @click="showAddStore = false">{{ t('common.cancel') }}</button>
            <button class="btn btn-primary" @click="addStore">{{ t('common.save') }}</button>
          </div>
        </div>
        
        <button v-else class="btn btn-secondary" @click="showAddStore = true">
          + {{ t('settings.addStore') }}
        </button>
      </div>
      
      <div v-if="saved" class="alert alert-success" style="margin-top: 24px;">
        {{ t('settings.saved') }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { usersApi, type SearchStore } from '@/api'

const { t, locale } = useI18n()
const authStore = useAuthStore()

const stores = ref<SearchStore[]>([])
const showAddStore = ref(false)
const newStoreName = ref('')
const newStoreUrl = ref('')
const saved = ref(false)

onMounted(() => {
  if (authStore.user) {
    stores.value = [...authStore.user.search_stores]
  }
  
  // Add default stores if empty
  if (stores.value.length === 0) {
    stores.value = [
      { name: 'Amazon', url: 'https://www.amazon.com/s?k={query}' },
      { name: 'eBay', url: 'https://www.ebay.com/sch/i.html?_nkw={query}' }
    ]
  }
})

async function changeLanguage(lang: string) {
  locale.value = lang
  localStorage.setItem('language', lang)
  await usersApi.updateLanguage(lang)
  authStore.updateLanguage(lang)
  showSaved()
}

async function addStore() {
  if (!newStoreName.value || !newStoreUrl.value) return
  
  stores.value.push({
    name: newStoreName.value,
    url: newStoreUrl.value
  })
  
  await usersApi.updateStores(stores.value)
  
  newStoreName.value = ''
  newStoreUrl.value = ''
  showAddStore.value = false
  showSaved()
}

async function removeStore(index: number) {
  stores.value.splice(index, 1)
  await usersApi.updateStores(stores.value)
  showSaved()
}

function showSaved() {
  saved.value = true
  setTimeout(() => { saved.value = false }, 3000)
}
</script>
