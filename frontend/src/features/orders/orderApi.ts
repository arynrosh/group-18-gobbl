import { api } from '../../api/client'
import type { CostBreakdown, Order, OrderStatusRecord } from '../../types'

export async function createOrder(params: {
  order_id: string
  restaurant_id: number
  delivery_distance: number
  delivery_time?: number | null
}): Promise<Order> {
  const { data } = await api.post<Order>('/orders', null, {
    params: {
      order_id: params.order_id,
      restaurant_id: params.restaurant_id,
      delivery_distance: params.delivery_distance,
      delivery_time: params.delivery_time ?? undefined,
    },
  })
  return data
}

export async function fetchOrder(orderId: string): Promise<Order> {
  const { data } = await api.get<Order>(`/orders/${orderId}`)
  return data
}

export async function addOrderItem(params: {
  orderId: string
  restaurant_id: number
  food_item: string
  quantity: number
}): Promise<Order> {
  const { data } = await api.post<Order>(`/orders/${params.orderId}/items`, null, {
    params: {
      restaurant_id: params.restaurant_id,
      food_item: params.food_item,
      quantity: params.quantity,
    },
  })
  return data
}

export async function removeOrderItem(orderId: string, foodItem: string): Promise<Order> {
  const encoded = encodeURIComponent(foodItem)
  const { data } = await api.delete<Order>(`/orders/${orderId}/items/${encoded}`)
  return data
}

export async function sendOrder(orderId: string): Promise<Order> {
  const { data } = await api.put<Order>(`/orders/${orderId}/send`)
  return data
}

export async function fetchOrderStatus(orderId: string): Promise<OrderStatusRecord> {
  const { data } = await api.get<OrderStatusRecord>(`/orders/${orderId}/status`)
  return data
}

export async function updateOrderStatus(orderId: string, msg: string): Promise<OrderStatusRecord> {
  const { data } = await api.put<OrderStatusRecord>(`/orders/${orderId}/status`, null, {
    params: { msg },
  })
  return data
}

export async function completeOrder(orderId: string): Promise<OrderStatusRecord> {
  const { data } = await api.put<OrderStatusRecord>(`/orders/${orderId}/complete`)
  return data
}

export async function calculateCost(orderId: string): Promise<CostBreakdown> {
  const { data } = await api.post<CostBreakdown>(`/cost/calculate/${orderId}`)
  return data
}

export async function addMysteryBag(
  orderId: string,
  budget: number,
): Promise<{ message: string; mystery_bag: { budget: number } }> {
  const { data } = await api.post(`/orders/${orderId}/mystery-bag`, { budget })
  return data
}

export async function fulfillOrder(orderId: string): Promise<{ order_id: string; fulfillment_status: string }> {
  const { data } = await api.post(`/orders/${orderId}/fulfill`)
  return data
}

export async function fetchFulfillmentStatus(
  orderId: string,
): Promise<{ order_id: string; fulfillment_status?: string }> {
  const { data } = await api.get(`/orders/${orderId}/fulfillment-status`)
  return data
}
