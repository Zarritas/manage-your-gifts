<template>
  <div>
    <nav class="navbar">
      <router-link to="/dashboard" class="navbar-brand">🎁 {{ t('app.name') }}</router-link>
    </nav>
    
    <div class="page container container-sm">
      <div class="page-header">
        <h1 class="page-title">{{ t('gifts.addGift') }}</h1>
      </div>
      
      <form class="card" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label class="form-label">{{ t('gifts.giftTitle') }} *</label>
          <input
            v-model="title"
            type="text"
            class="form-input"
            :placeholder="t('gifts.titlePlaceholder')"
            required
            autofocus
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">{{ t('gifts.description') }}</label>
          <textarea
            v-model="description"
            class="form-input"
            :placeholder="t('gifts.descriptionPlaceholder')"
            rows="3"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label class="form-label">{{ t('gifts.price') }}</label>
          <input
            v-model.number="price"
            type="number"
            step="0.01"
            min="0"
            class="form-input"
            :placeholder="t('gifts.pricePlaceholder')"
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">{{ t('gifts.link') }}</label>
          <input
            v-model="link"
            type="url"
            class="form-input"
            :placeholder="t('gifts.linkPlaceholder')"
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">{{ t('gifts.imageUrl') }}</label>
          <input
            v-model="imageUrl"
            type="url"
            class="form-input"
            placeholder="https://example.com/image.jpg"
          />
        </div>
        
        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>
        
        <div style="display: flex; gap: 12px; margin-top: 24px;">
          <router-link :to="`/groups/${groupId}`" class="btn btn-secondary" style="flex: 1;">
            {{ t('common.cancel') }}
          </router-link>
          <button type="submit" class="btn btn-primary" style="flex: 1;" :disabled="loading">
            {{ loading ? t('common.loading') : t('gifts.create') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { giftsApi } from '@/api'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

const groupId = computed(() => route.params.id as string)

const title = ref('')
const description = ref('')
const price = ref<number | undefined>(undefined)
const link = ref('')
const imageUrl = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

async function handleSubmit() {
  loading.value = true
  error.value = null
  
  try {
    await giftsApi.create(groupId.value, {
      title: title.value,
      description: description.value || undefined,
      price: price.value || undefined,
      link: link.value || undefined,
      image_url: imageUrl.value || undefined
    })
    router.push(`/groups/${groupId.value}`)
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>
