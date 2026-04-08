import { api } from '../../api/client'
import type { PaymentMethodResponse, SavePaymentMethodRequest } from '../../types'

export async function listPaymentMethods(): Promise<PaymentMethodResponse[]> {
  const { data } = await api.get<PaymentMethodResponse[]>('/payment-methods')
  return data
}

export async function savePaymentMethod(payload: SavePaymentMethodRequest): Promise<PaymentMethodResponse> {
  const { data } = await api.post<PaymentMethodResponse>('/payment-methods', payload)
  return data
}

export async function deletePaymentMethod(methodId: string): Promise<void> {
  await api.delete(`/payment-methods/${encodeURIComponent(methodId)}`)
}
