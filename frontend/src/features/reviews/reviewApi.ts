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

export interface RestaurantReview {
  review_id: number
  order_id: string
  restaurant_id: number
  customer_id: string
  food_temperature: string
  food_freshness: number
  packaging_quality: number
  food_condition: string
  item_ratings: Array<{
    menu_item_id: number
    food_item: string
    customer_rating: number
    written_review?: string | null
  }>
}

export async function getRestaurantReviews(restaurantId: number): Promise<RestaurantReview[]> {
  const { data } = await api.get<RestaurantReview[]>(`/reviews/restaurant/${restaurantId}`)
  return data
}

export async function getRestaurantAverageRating(restaurantId: number): Promise<{ average_rating: number }> {
  const { data } = await api.get<{ average_rating: number }>(`/reviews/restaurant/${restaurantId}/average`)
  return data
}
