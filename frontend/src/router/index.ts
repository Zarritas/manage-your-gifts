import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'login',
            component: () => import('@/views/LoginView.vue'),
            meta: { guest: true }
        },
        {
            path: '/dashboard',
            name: 'dashboard',
            component: () => import('@/views/DashboardView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/groups/new',
            name: 'create-group',
            component: () => import('@/views/CreateGroupView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/groups/:id',
            name: 'group',
            component: () => import('@/views/GroupDetailView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/groups/:id/gifts/new',
            name: 'add-gift',
            component: () => import('@/views/AddGiftView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/join/:id',
            name: 'join-group',
            component: () => import('@/views/JoinGroupView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/settings',
            name: 'settings',
            component: () => import('@/views/SettingsView.vue'),
            meta: { requiresAuth: true }
        }
    ]
})

router.beforeEach((to, _from, next) => {
    const authStore = useAuthStore()

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        // Save intended destination
        localStorage.setItem('redirectTo', to.fullPath)
        next({ name: 'login' })
    } else if (to.meta.guest && authStore.isAuthenticated) {
        next({ name: 'dashboard' })
    } else {
        next()
    }
})

export default router
