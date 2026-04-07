import { api } from '../../api/client'
import type { Notification, NotificationRequest } from '../../types'

export async function getCustomerNotifications(customerId: string): Promise<Notification[]> {
  const { data } = await api.get<Notification[]>(`/notifications/customer/${encodeURIComponent(customerId)}`)
  return data
}

export async function getRestaurantNotifications(restaurantId: number): Promise<Notification[]> {
  const { data } = await api.get<Notification[]>(`/notifications/restaurant/${restaurantId}`)
  return data
}

export async function sendNotification(payload: NotificationRequest): Promise<Notification> {
  const { data } = await api.post<Notification>('/notifications/send', payload)
  return data
}

export async function orderPlaced(payload: {
  order_id: string
  customer_id: string
  restaurant_id: number
}): Promise<Notification> {
  const { data } = await api.post<Notification>('/order-notifications/placed', payload)
  return data
}

export async function orderOutForDelivery(payload: {
  order_id: string
  customer_id: string
  restaurant_id: number
  driver_name: string
}): Promise<Notification> {
  const { data } = await api.post<Notification>('/order-notifications/out-for-delivery', payload)
  return data
}

export async function orderDelivered(payload: {
  order_id: string
  customer_id: string
  restaurant_id: number
}): Promise<Notification> {
  const { data } = await api.post<Notification>('/order-notifications/delivered', payload)
  return data
}

export async function orderDelayed(payload: {
  order_id: string
  customer_id: string
  restaurant_id: number
  delay_minutes: number
}): Promise<Notification> {
  const { data } = await api.post<Notification>('/order-notifications/delayed', payload)
  return data
}
