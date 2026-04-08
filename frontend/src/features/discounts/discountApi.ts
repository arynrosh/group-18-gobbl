import { api } from '../../api/client'
import type { CreateDiscountRequest, DiscountResponse } from '../../types'

export async function getMyDiscountCodes(): Promise<DiscountResponse[]> {
  const { data } = await api.get<DiscountResponse[]>('/discounts/my-codes')
  return data
}

export async function getAllDiscounts(): Promise<DiscountResponse[]> {
  const { data } = await api.get<DiscountResponse[]>('/discounts')
  return data
}

export async function createDiscount(payload: CreateDiscountRequest): Promise<DiscountResponse> {
  const { data } = await api.post<DiscountResponse>('/discounts', payload)
  return data
}
