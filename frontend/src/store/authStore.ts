import { create } from 'zustand'
import type { UserInfo, UserRole } from '../types'
import { api } from '../api/client'

const TOKEN_KEY = 'gobbl_token'

function readToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

interface AuthState {
  token: string | null
  user: UserInfo | null
  bootstrapped: boolean
  setToken: (t: string | null) => void
  setUser: (u: UserInfo | null) => void
  logout: () => void
  fetchMe: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set, get) => ({
  token: readToken(),
  user: null,
  bootstrapped: false,
  setToken: (token) => {
    if (token) localStorage.setItem(TOKEN_KEY, token)
    else localStorage.removeItem(TOKEN_KEY)
    set({ token })
  },
  setUser: (user) => set({ user }),
  logout: () => {
    localStorage.removeItem(TOKEN_KEY)
    set({ token: null, user: null, bootstrapped: true })
  },
  fetchMe: async () => {
    const { token } = get()
    if (!token) {
      set({ user: null, bootstrapped: true })
      return
    }
    try {
      const { data } = await api.get<UserInfo>('/auth/me')
      set({ user: data, bootstrapped: true })
    } catch {
      localStorage.removeItem(TOKEN_KEY)
      set({ token: null, user: null, bootstrapped: true })
    }
  },
}))

export function hasRole(user: UserInfo | null, roles: UserRole[]): boolean {
  if (!user) return false
  return roles.includes(user.role as UserRole)
}
