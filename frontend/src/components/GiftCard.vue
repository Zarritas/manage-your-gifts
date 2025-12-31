<template>
  <div class="card gift-card">
    <!-- Status Badge (only for non-owners) -->
    <div v-if="!gift.is_own && gift.reservation_status" class="gift-status">
      <span v-if="gift.reservation_status === 'reserved'" class="badge badge-warning">
        {{ t('gifts.reserved') }}
      </span>
      <span v-else-if="gift.reservation_status === 'purchased'" class="badge badge-success">
        {{ t('gifts.purchased') }}
      </span>
    </div>
    
    <!-- My Gift Badge -->
    <div v-if="gift.is_own" class="gift-status">
      <span class="badge badge-info">{{ t('gifts.myGift') }}</span>
    </div>
    
    <!-- Image -->
    <div v-if="gift.image_url" class="gift-card-image-container">
      <img :src="gift.image_url" :alt="gift.title" class="gift-card-image" />
    </div>
    <div v-else class="gift-card-image gift-card-placeholder">
      🎁
    </div>
    
    <!-- Content -->
    <h3 class="gift-card-title">{{ gift.title }}</h3>
    <p class="gift-card-owner">{{ gift.owner_email }}</p>
    
    <p v-if="gift.description" style="font-size: 14px; color: var(--text-secondary); margin-bottom: 8px;">
      {{ gift.description }}
    </p>
    
    <p v-if="gift.price" class="gift-card-price">
      {{ formatPrice(gift.price) }}
    </p>
    
    <!-- Search Links (for non-owners) -->
    <div v-if="!gift.is_own" class="search-links" style="margin-top: 12px;">
      <a 
        v-for="store in searchStores" 
        :key="store.name"
        :href="getSearchUrl(store.url, gift.title)"
        target="_blank"
        class="search-link"
      >
        {{ t('gifts.searchOn') }} {{ store.name }} →
      </a>
    </div>
    
    <!-- Actions -->
    <div class="gift-card-actions">
      <!-- Owner Actions -->
      <template v-if="gift.is_own">
        <button 
          v-if="groupStatus === 'active'"
          class="btn btn-danger btn-sm" 
          @click="$emit('delete')"
        >
          {{ t('gifts.delete') }}
        </button>
        <a 
          v-if="gift.link" 
          :href="gift.link" 
          target="_blank" 
          class="btn btn-secondary btn-sm"
        >
          🔗 Link
        </a>
      </template>
      
      <!-- Non-Owner Actions -->
      <template v-else>
        <!-- Free Gift -->
        <template v-if="!gift.reservation_status && groupStatus === 'active'">
          <button class="btn btn-primary btn-sm" @click="$emit('reserve')">
            {{ t('gifts.reserve') }}
          </button>
        </template>
        
        <!-- Reserved by me -->
        <template v-if="gift.reserved_by_me">
          <button 
            v-if="gift.reservation_status === 'reserved'" 
            class="btn btn-secondary btn-sm" 
            @click="$emit('unreserve')"
          >
            {{ t('gifts.unreserve') }}
          </button>
          <button 
            v-if="gift.reservation_status === 'reserved'" 
            class="btn btn-success btn-sm" 
            @click="$emit('mark-purchased')"
          >
            {{ t('gifts.markPurchased') }}
          </button>
        </template>
        
        <a 
          v-if="gift.link" 
          :href="gift.link" 
          target="_blank" 
          class="btn btn-secondary btn-sm"
        >
          🔗 Link
        </a>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import type { Gift } from '@/api'

const { t } = useI18n()
const authStore = useAuthStore()

const props = defineProps<{
  gift: Gift
  groupStatus: string
}>()

defineEmits<{
  reserve: []
  unreserve: []
  'mark-purchased': []
  delete: []
}>()

const searchStores = computed(() => {
  if (authStore.user?.search_stores?.length) {
    return authStore.user.search_stores
  }
  return [
    { name: 'Amazon', url: 'https://www.amazon.com/s?k={query}' },
    { name: 'Google', url: 'https://www.google.com/search?q={query}' }
  ]
})

function formatPrice(price: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'EUR'
  }).format(price)
}

function getSearchUrl(baseUrl: string, query: string): string {
  return baseUrl.replace('{query}', encodeURIComponent(query))
}
</script>

<style scoped>
.gift-card-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
}
</style>
