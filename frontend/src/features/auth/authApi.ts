import { api } from '../../api/client'
import type { TokenResponse, UserInfo, RegisterRequest, UserResponse } from '../../types'

export async function login(username: string, password: string): Promise<TokenResponse> {
  const body = new URLSearchParams()
  body.set('username', username)
  body.set('password', password)
  const { data } = await api.post<TokenResponse>('/auth/login', body, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return data
}

export async function register(payload: RegisterRequest): Promise<UserResponse> {
  const { data } = await api.post<UserResponse>('/users/register', payload)
  return data
}

export async function fetchMe(): Promise<UserInfo> {
  const { data } = await api.get<UserInfo>('/auth/me')
  return data
}
