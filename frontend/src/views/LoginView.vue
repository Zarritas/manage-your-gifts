<template>
  <div class="login-container">
    <div class="card login-card card-glass">
      <div class="login-header">
        <div class="login-logo">🎁</div>
        <h1 class="login-title">{{ t('app.name') }}</h1>
        <p class="login-subtitle">{{ t('app.tagline') }}</p>
      </div>
      
      <!-- Step 1: Email -->
      <form v-if="step === 'email'" @submit.prevent="handleSendCode">
        <div class="form-group">
          <label class="form-label">{{ t('auth.email') }}</label>
          <input
            v-model="email"
            type="email"
            class="form-input form-input-lg"
            :placeholder="t('auth.emailPlaceholder')"
            required
            autofocus
          />
        </div>
        
        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>
        
        <button type="submit" class="btn btn-primary btn-lg btn-block" :disabled="loading">
          {{ loading ? t('common.loading') : t('auth.sendCode') }}
        </button>
      </form>
      
      <!-- Step 2: OTP -->
      <form v-else @submit.prevent="handleVerifyCode">
        <div class="form-group">
          <label class="form-label">{{ t('auth.enterCode') }}</label>
          <div class="otp-container">
            <input
              v-for="i in 6"
              :key="i"
              :ref="el => otpRefs[i-1] = el"
              v-model="otp[i-1]"
              type="text"
              maxlength="1"
              class="form-input otp-input"
              @input="handleOtpInput(i-1)"
              @keydown.backspace="handleOtpBackspace(i-1, $event)"
              @paste="handleOtpPaste"
            />
          </div>
        </div>
        
        <p class="alert alert-success">{{ t('auth.codeSent') }}</p>
        
        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>
        
        <button type="submit" class="btn btn-primary btn-lg btn-block" :disabled="loading">
          {{ loading ? t('common.loading') : t('auth.verifyCode') }}
        </button>
        
        <button type="button" class="btn btn-ghost btn-block" @click="step = 'email'" style="margin-top: 12px">
          {{ t('common.back') }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const authStore = useAuthStore()

const step = ref<'email' | 'otp'>('email')
const email = ref('')
const otp = ref<string[]>(['', '', '', '', '', ''])
const otpRefs = ref<(HTMLInputElement | null)[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

async function handleSendCode() {
  loading.value = true
  error.value = null
  
  const success = await authStore.sendCode(email.value)
  
  if (success) {
    step.value = 'otp'
    setTimeout(() => otpRefs.value[0]?.focus(), 100)
  } else {
    error.value = authStore.error
  }
  
  loading.value = false
}

async function handleVerifyCode() {
  const code = otp.value.join('')
  if (code.length !== 6) return
  
  loading.value = true
  error.value = null
  
  const success = await authStore.verifyCode(email.value, code)
  
  if (!success) {
    error.value = t('auth.invalidCode')
    otp.value = ['', '', '', '', '', '']
    otpRefs.value[0]?.focus()
  }
  
  loading.value = false
}

function handleOtpInput(index: number) {
  if (otp.value[index] && index < 5) {
    otpRefs.value[index + 1]?.focus()
  }
}

function handleOtpBackspace(index: number, event: KeyboardEvent) {
  if (!otp.value[index] && index > 0) {
    otpRefs.value[index - 1]?.focus()
  }
}

function handleOtpPaste(event: ClipboardEvent) {
  event.preventDefault()
  const paste = event.clipboardData?.getData('text') || ''
  const digits = paste.replace(/\D/g, '').slice(0, 6).split('')
  digits.forEach((d, i) => { otp.value[i] = d })
  otpRefs.value[Math.min(digits.length, 5)]?.focus()
}
</script>
