import { browseAllRestaurants } from './restaurantApi'
import { getRestaurantAverageRating, getRestaurantReviews } from '../reviews/reviewApi'
import { getPopularByOrders } from '../admin/statisticsApi'
import type { Restaurant } from '../../types'

export type PopularOrderRow = { restaurant_id: number; total_orders: number }

/** Backend: GET /statistics/popular-restaurants/orders */
export async function fetchPopularOrderRows(limit = 50): Promise<PopularOrderRow[]> {
  const data = await getPopularByOrders(limit)
  if (!Array.isArray(data)) return []
  return data
    .map((row: { restaurant_id: number | string; total_orders?: number }) => ({
      restaurant_id: Number(row.restaurant_id),
      total_orders: Number(row.total_orders ?? 0),
    }))
    .filter((r) => Number.isFinite(r.restaurant_id))
}

/**
 * Restaurants ordered by order count (statistics API), intersected with browse catalog.
 * Returns rows in popularity order for pagination on the client.
 */
export async function fetchRestaurantsRankedByOrders(max = 100): Promise<{
  restaurants: Restaurant[]
  orderCountById: Record<number, number>
}> {
  const [rows, catalogItems] = await Promise.all([fetchPopularOrderRows(max), browseAllRestaurants()])
  const byId = new Map(catalogItems.map((r) => [r.restaurant_id, r]))
  const restaurants: Restaurant[] = []
  const orderCountById: Record<number, number> = {}
  for (const row of rows) {
    const r = byId.get(row.restaurant_id)
    if (r) {
      restaurants.push(r)
      orderCountById[row.restaurant_id] = row.total_orders
    }
  }
  return { restaurants, orderCountById }
}

/**
 * Average of every item_rating.customer_rating across all reviews for the restaurant
 * (GET /reviews/restaurant/:id). Aligns with review cards, not menu-derived averages.
 */
export async function fetchRestaurantsRankedByAggregatedReviewRatings(
  browseLimit = 200,
  topN = 10,
): Promise<{ restaurants: Restaurant[]; ratingById: Record<number, number> }> {
  const all = await browseAllRestaurants()
  const items = all.slice(0, Math.min(browseLimit, all.length))
  const settled = await Promise.allSettled(
    items.map(async (r) => {
      const reviews = await getRestaurantReviews(r.restaurant_id)
      const vals: number[] = []
      for (const rev of reviews) {
        if (!Array.isArray(rev.item_ratings)) continue
        for (const it of rev.item_ratings) {
          const n = Number(it.customer_rating)
          if (Number.isFinite(n)) vals.push(n)
        }
      }
      if (vals.length === 0) return null
      const average_rating = Math.round((vals.reduce((a, b) => a + b, 0) / vals.length) * 100) / 100
      return { restaurant: r, average_rating }
    }),
  )
  const scored = settled
    .filter((x): x is PromiseFulfilledResult<{ restaurant: Restaurant; average_rating: number } | null> => x.status === 'fulfilled')
    .map((x) => x.value)
    .filter((x): x is { restaurant: Restaurant; average_rating: number } => x != null)
  scored.sort((a, b) => b.average_rating - a.average_rating)
  const sliced = scored.slice(0, topN)
  const ratingById: Record<number, number> = {}
  for (const x of sliced) ratingById[x.restaurant.restaurant_id] = x.average_rating
  return {
    restaurants: sliced.map((x) => x.restaurant),
    ratingById,
  }
}

/**
 * Popular-by-rating using GET /reviews/restaurant/:id/average (menu item customer_rating only).
 * Prefer fetchRestaurantsRankedByAggregatedReviewRatings when rankings should match submitted reviews.
 */
export async function fetchRestaurantsRankedByAverageRating(max = 100): Promise<{
  restaurants: Restaurant[]
  ratingById: Record<number, number>
}> {
  const items = await browseAllRestaurants()
  const scored = await Promise.all(
    items.map(async (r) => {
      try {
        const { average_rating } = await getRestaurantAverageRating(r.restaurant_id)
        const n = Number(average_rating)
        if (!Number.isFinite(n)) return null
        return { restaurant: r, average_rating: n }
      } catch {
        return null
      }
    }),
  )
  const ok = scored.filter((x): x is NonNullable<typeof x> => x != null)
  ok.sort((a, b) => b.average_rating - a.average_rating)
  const sliced = ok.slice(0, max)
  const ratingById: Record<number, number> = {}
  for (const x of sliced) {
    ratingById[x.restaurant.restaurant_id] = x.average_rating
  }
  return {
    restaurants: sliced.map((x) => x.restaurant),
    ratingById,
  }
}
