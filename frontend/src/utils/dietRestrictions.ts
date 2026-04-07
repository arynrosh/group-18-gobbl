import type { DietRestrictionsEntry, Order } from '../types'

export function normalizeOrderDietRestrictions(order: Order | null): DietRestrictionsEntry | null {
  if (!order || order.diet_restrictions == null) return null
  const raw = order.diet_restrictions
  if (Array.isArray(raw)) {
    return { username: order.customer_id, diet_restrictions: raw }
  }
  if (typeof raw === 'object' && raw && 'diet_restrictions' in raw) {
    const row = raw as DietRestrictionsEntry
    return {
      username: row.username ?? order.customer_id,
      diet_restrictions: Array.isArray(row.diet_restrictions) ? row.diet_restrictions : [],
    }
  }
  return null
}
