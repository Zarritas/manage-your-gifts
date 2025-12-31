import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from './auth'

export const useSocketStore = defineStore('socket', () => {
    const socket = ref<WebSocket | null>(null)
    const isConnected = ref(false)
    const listeners = ref<Function[]>([])

    function connect() {
        const authStore = useAuthStore()
        if (!authStore.token || isConnected.value) return

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
        // Use 127.0.0.1 directly as per Vite config fix, or relative path if proxied
        // Since websocket doesn't go through http proxy easily in dev without specific config,
        // let's point to backend directly. 
        // Backend runs on port 8000.
        const host = window.location.hostname === 'localhost' ? '127.0.0.1:8000' : window.location.host
        // If production, use relative 'ws', in dev use direct 8000
        const wsUrl = import.meta.env.DEV
            ? `ws://127.0.0.1:8000/ws`
            : `${protocol}//${host}/ws`

        console.log('Connecting WS to:', wsUrl)

        socket.value = new WebSocket(`${wsUrl}?token=${authStore.token}`)

        socket.value.onopen = () => {
            console.log('WS Connected')
            isConnected.value = true
        }

        socket.value.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data)
                console.log('WS Message:', data)
                notifyListeners(data)
            } catch (e) {
                console.error('Error parsing WS message', e)
            }
        }

        socket.value.onclose = () => {
            console.log('WS Disconnected')
            isConnected.value = false
            socket.value = null
            // Simple reconnect logic
            setTimeout(() => {
                if (authStore.isAuthenticated) connect()
            }, 3000)
        }
    }

    function disconnect() {
        if (socket.value) {
            socket.value.close()
            socket.value = null
            isConnected.value = false
        }
    }

    function onMessage(callback: (data: any) => void) {
        listeners.value.push(callback)
    }

    function removeListener(callback: (data: any) => void) {
        listeners.value = listeners.value.filter(l => l !== callback)
    }

    function notifyListeners(data: any) {
        listeners.value.forEach(cb => cb(data))
    }

    return {
        isConnected,
        connect,
        disconnect,
        onMessage,
        removeListener
    }
})
