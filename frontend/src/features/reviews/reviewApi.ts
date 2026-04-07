import { api } from '../../api/client'
import type { ReviewCreate, ReviewableItem } from '../../types'

export async function submitReview(review: ReviewCreate): Promise<{ message: string; review: unknown }> {
  const { data } = await api.post('/reviews/', review)
  return data
}

export async function getReviewableItems(orderId: string): Promise<{
  order_id: string
  items: ReviewableItem[]
}> {
  const { data } = await api.get(`/reviews/order/${orderId}/items`)
  return data
}

export async function getRestaurantReviews(restaurantId: number): Promise<unknown[]> {
  const { data } = await api.get<unknown[]>(`/reviews/restaurant/${restaurantId}`)
  return data
}

export async function getRestaurantAverageRating(restaurantId: number): Promise<{ average_rating: number }> {
  const { data } = await api.get<{ average_rating: number }>(`/reviews/restaurant/${restaurantId}/average`)
  return data
}
