import { api } from '../../api/client'
import type { MenuItem, Paginated, Restaurant } from '../../types'

export async function browseRestaurants(limit = 20, offset = 0): Promise<Paginated<Restaurant>> {
  const { data } = await api.get<Paginated<Restaurant>>('/browse/restaurants', {
    params: { limit, offset },
  })
  return data
}

export async function searchRestaurantsByName(
  name: string,
  limit = 20,
  offset = 0,
): Promise<Paginated<Restaurant>> {
  const { data } = await api.get<Paginated<Restaurant>>('/restaurant/search/name', {
    params: { name, limit, offset },
  })
  return data
}

export async function searchRestaurantsByCuisine(
  cuisine: string,
  limit = 20,
  offset = 0,
): Promise<Paginated<Restaurant>> {
  const { data } = await api.get<Paginated<Restaurant>>('/restaurant/search/cuisine', {
    params: { cuisine, limit, offset },
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
    params: { name, limit, offset },
  })
  return data
}
