<template>
  <div class="invite-container">
    <h3 style="margin-bottom: 16px;">{{ t('groups.invite') }}</h3>
    
    <!-- QR Code -->
    <div class="invite-qr">
      <QRCodeVue :value="inviteUrl" :size="180" />
    </div>
    
    <!-- Invite Link -->
    <div class="invite-link">
      <input 
        ref="linkInput"
        type="text" 
        class="form-input" 
        :value="inviteUrl" 
        readonly 
      />
      <button class="btn btn-primary" @click="copyLink">
        {{ copied ? '✓' : t('groups.copyLink') }}
      </button>
    </div>
    
    <p v-if="copied" style="color: var(--success); margin-top: 8px; font-size: 14px;">
      {{ t('groups.linkCopied') }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import QRCodeVue from 'qrcode.vue'

const { t } = useI18n()

const props = defineProps<{
  groupId: string
}>()

const copied = ref(false)
const linkInput = ref<HTMLInputElement | null>(null)

const inviteUrl = computed(() => {
  return `${window.location.origin}/join/${props.groupId}`
})

async function copyLink() {
  try {
    await navigator.clipboard.writeText(inviteUrl.value)
    copied.value = true
    setTimeout(() => { copied.value = false }, 3000)
  } catch {
    linkInput.value?.select()
    document.execCommand('copy')
    copied.value = true
    setTimeout(() => { copied.value = false }, 3000)
  }
}
</script>
