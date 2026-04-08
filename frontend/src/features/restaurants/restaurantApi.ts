import { api } from '../../api/client'
import type { MenuItem, Paginated, Restaurant } from '../../types'

/** Matches app/schemas/pagination_schema.py: PaginationParams limit le=100 */
export const BROWSE_RESTAURANTS_MAX_LIMIT = 100

function clampPageLimit(limit: number): number {
  return Math.min(Math.max(1, limit), BROWSE_RESTAURANTS_MAX_LIMIT)
}

export async function browseRestaurants(limit = 20, offset = 0): Promise<Paginated<Restaurant>> {
  const { data } = await api.get<Paginated<Restaurant>>('/browse/restaurants', {
    params: { limit: clampPageLimit(limit), offset },
  })
  return data
}

/** Loads every restaurant via repeated browse calls (max 100 rows per request). */
export async function browseAllRestaurants(): Promise<Restaurant[]> {
  const out: Restaurant[] = []
  let offset = 0
  for (;;) {
    const page = await browseRestaurants(BROWSE_RESTAURANTS_MAX_LIMIT, offset)
    out.push(...page.items)
    if (page.items.length === 0 || out.length >= page.total) break
    offset += BROWSE_RESTAURANTS_MAX_LIMIT
  }
  return out
}

export async function searchRestaurantsByName(
  name: string,
  limit = 20,
  offset = 0,
): Promise<Paginated<Restaurant>> {
  const { data } = await api.get<Paginated<Restaurant>>('/restaurant/search/name', {
    params: { name, limit: clampPageLimit(limit), offset },
  })
  return data
}

export async function searchRestaurantsByCuisine(
  cuisine: string,
  limit = 20,
  offset = 0,
): Promise<Paginated<Restaurant>> {
  const { data } = await api.get<Paginated<Restaurant>>('/restaurant/search/cuisine', {
    params: { cuisine, limit: clampPageLimit(limit), offset },
  })
  return data
}

export async function fetchMenu(
  restaurantId: number,
  params?: { price_tier?: string; min_rating?: number },
): Promise<MenuItem[]> {
  const { data } = await api.get<MenuItem[]>(`/menu/${restaurantId}`, { params })
  return data
}

export async function searchMenuByName(
  name: string,
  limit = 20,
  offset = 0,
): Promise<Paginated<MenuItem>> {
  const { data } = await api.get<Paginated<MenuItem>>('/menu/search/name', {
    params: { name, limit: clampPageLimit(limit), offset },
  })
  return data
}
