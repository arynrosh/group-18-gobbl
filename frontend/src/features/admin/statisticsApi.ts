import { api } from '../../api/client'

export async function getDeliveryTimes(): Promise<unknown> {
  const { data } = await api.get('/statistics/delivery-times')
  return data
}

export async function getPopularByOrders(limit = 10): Promise<unknown> {
  const { data } = await api.get('/statistics/popular-restaurants/orders', { params: { limit } })
  return data
}

export async function getPopularByRatings(limit = 10): Promise<unknown> {
  const { data } = await api.get('/statistics/popular-restaurants/ratings', { params: { limit } })
  return data
}
