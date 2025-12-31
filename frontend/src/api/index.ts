const API_BASE = '/api'

async function request<T>(
    endpoint: string,
    options: RequestInit = {}
): Promise<T> {
    const token = localStorage.getItem('token')

    const headers: HeadersInit = {
        'Content-Type': 'application/json',
        ...options.headers
    }

    if (token) {
        (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers
    })

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Network error' }))
        throw new Error(error.detail || 'Request failed')
    }

    return response.json()
}

// Auth API
export const authApi = {
    sendCode: (email: string) =>
        request<{ success: boolean; message: string }>('/auth/send-code', {
            method: 'POST',
            body: JSON.stringify({ email })
        }),

    verifyCode: (email: string, code: string) =>
        request<{ success: boolean; message: string; token: string }>('/auth/verify-code', {
            method: 'POST',
            body: JSON.stringify({ email, code })
        }),

    me: () => request<User>('/auth/me')
}

// Groups API
export const groupsApi = {
    list: () => request<Group[]>('/groups'),

    create: (name: string, description?: string) =>
        request<Group>('/groups', {
            method: 'POST',
            body: JSON.stringify({ name, description })
        }),

    get: (id: string) => request<GroupDetail>(`/groups/${id}`),

    join: (id: string) =>
        request<{ success: boolean; message: string }>(`/groups/${id}/join`, {
            method: 'POST'
        }),

    acceptMember: (groupId: string, userId: string) =>
        request<{ success: boolean }>(`/groups/${groupId}/members/${userId}/accept`, {
            method: 'POST'
        }),

    rejectMember: (groupId: string, userId: string) =>
        request<{ success: boolean }>(`/groups/${groupId}/members/${userId}/reject`, {
            method: 'POST'
        }),

    removeMember: (groupId: string, userId: string) =>
        request<{ success: boolean }>(`/groups/${groupId}/members/${userId}`, {
            method: 'DELETE'
        }),

    close: (id: string) =>
        request<{ success: boolean }>(`/groups/${id}/close`, {
            method: 'POST'
        })
}

// Gifts API
export const giftsApi = {
    list: (groupId: string) => request<Gift[]>(`/groups/${groupId}/gifts`),

    create: (groupId: string, data: CreateGiftData) =>
        request<Gift>(`/groups/${groupId}/gifts`, {
            method: 'POST',
            body: JSON.stringify(data)
        }),

    delete: (groupId: string, id: string) =>
        request<{ success: boolean }>(`/groups/${groupId}/gifts/${id}`, {
            method: 'DELETE'
        }),

    reserve: (id: string) =>
        request<{ success: boolean }>(`/gifts/${id}/reserve`, {
            method: 'POST'
        }),

    unreserve: (id: string) =>
        request<{ success: boolean }>(`/gifts/${id}/reserve`, {
            method: 'DELETE'
        }),

    markPurchased: (id: string) =>
        request<{ success: boolean }>(`/gifts/${id}/purchased`, {
            method: 'POST'
        })
}

// Users API
export const usersApi = {
    updateLanguage: (language: string) =>
        request<User>('/users/me/language', {
            method: 'PATCH',
            body: JSON.stringify({ language })
        }),

    updateStores: (stores: SearchStore[]) =>
        request<User>('/users/me/stores', {
            method: 'PATCH',
            body: JSON.stringify({ stores })
        })
}

// Types
export interface User {
    id: string
    email: string
    language: string
    search_stores: SearchStore[]
    created_at: string
}

export interface SearchStore {
    name: string
    url: string
}

export interface Group {
    id: string
    name: string
    description?: string
    status: 'active' | 'closed'
    admin_user_id: string
    created_at: string
    member_count: number
    is_admin?: boolean
}

export interface GroupMember {
    id: string
    user_id: string
    email: string
    status: 'pending' | 'accepted' | 'rejected'
    joined_at?: string
    is_admin: boolean
}

export interface GroupDetail extends Group {
    members: GroupMember[]
}

export interface Gift {
    id: string
    group_id: string
    owner_user_id: string
    owner_email: string
    title: string
    description?: string
    image_url?: string
    price?: number
    link?: string
    created_at: string
    is_own: boolean
    reservation_status?: 'reserved' | 'purchased' | null
    reserved_by_me: boolean
}

export interface CreateGiftData {
    title: string
    description?: string
    image_url?: string
    price?: number
    link?: string
}
