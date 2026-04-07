import { api } from '../../api/client'
import type { PaymentRequest, PaymentResponse, PaymentRecord } from '../../types'

export async function processPayment(payload: PaymentRequest): Promise<PaymentResponse> {
  const { data } = await api.post<PaymentResponse>('/payments/process', payload)
  return data
}

export async function getPaymentByOrder(orderId: string): Promise<PaymentRecord> {
  const { data } = await api.get<PaymentRecord>(`/payments/order/${orderId}`)
  return data
}

export async function getPaymentByTransaction(transactionId: string): Promise<PaymentRecord> {
  const { data } = await api.get<PaymentRecord>(`/payments/transaction/${transactionId}`)
  return data
}
