import { api } from '../../api/client'
import type { MenuItem } from '../../types'

export interface MenuItemCreate {
  restaurant_name: string
  cuisine: string
  food_item: string
  order_value: number
}

export interface MenuItemUpdate {
  restaurant_name?: string
  cuisine?: string
  food_item?: string
  order_value?: number
}

export async function createMenuItem(
  restaurantId: number,
  payload: MenuItemCreate,
): Promise<{ message: string; item: MenuItem }> {
  const { data } = await api.post(`/menu/${restaurantId}`, payload)
  return data
}

export async function updateMenuItem(
  restaurantId: number,
  menuId: number,
  payload: MenuItemUpdate,
): Promise<{ message: string; item: MenuItem }> {
  const { data } = await api.put(`/menu/${restaurantId}/${menuId}`, payload)
  return data
}

export async function deleteMenuItem(restaurantId: number, menuId: number): Promise<{ message: string }> {
  const { data } = await api.delete(`/menu/${restaurantId}/${menuId}`)
  return data
}
