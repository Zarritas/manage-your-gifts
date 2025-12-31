import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type User } from '@/api'
import { useI18n } from 'vue-i18n'
import { useSocketStore } from './socket'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
    const { locale } = useI18n()
    const user = ref<User | null>(null)
    const token = ref<string | null>(localStorage.getItem('token'))
    const loading = ref(false)
    const error = ref<string | null>(null)

    const isAuthenticated = computed(() => !!token.value)

    async function checkAuth() {
        if (!token.value) return

        try {
            loading.value = true
            user.value = await authApi.me()
            // Update language
            localStorage.setItem('language', user.value.language)
        } catch (e) {
            // Token invalid
            logout()
        } finally {
            loading.value = false
        }
    }

    async function sendCode(email: string): Promise<boolean> {
        try {
            loading.value = true
            error.value = null
            await authApi.sendCode(email)
            return true
        } catch (e: any) {
            error.value = e.message
            return false
        } finally {
            loading.value = false
        }
    }

    async function verifyCode(email: string, code: string): Promise<boolean> {
        try {
            loading.value = true
            error.value = null
            const response = await authApi.verifyCode(email, code)

            token.value = response.token
            localStorage.setItem('token', response.token)

            // Fetch user
            await checkAuth()

            // Connect socket
            const socketStore = useSocketStore()
            socketStore.connect()

            // Redirect
            const redirectTo = localStorage.getItem('redirectTo') || '/dashboard'
            localStorage.removeItem('redirectTo')
            router.push(redirectTo)

            return true
        } catch (e: any) {
            error.value = e.message
            return false
        } finally {
            loading.value = false
        }
    }

    function logout() {
        user.value = null
        token.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('user') // Added removal of 'user' from localStorage

        // Disconnect socket
        const socketStore = useSocketStore()
        socketStore.disconnect()

        router.push('/')
    }

    async function updateLanguage(language: string) {
        if (user.value) {
            user.value.language = language
            locale.value = language // Set locale
            localStorage.setItem('language', language)
        }
    }

    // Initialize socket if logged in
    if (token.value) {
        const socketStore = useSocketStore()
        socketStore.connect()
    }

    return {
        user,
        token,
        loading,
        error,
        isAuthenticated,
        checkAuth,
        sendCode,
        verifyCode,
        logout,
        updateLanguage
    }
})
