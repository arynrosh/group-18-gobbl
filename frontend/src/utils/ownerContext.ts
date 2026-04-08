const KEY = 'gobbl_owner_restaurant_id'

export function getOwnerRestaurantId(): number | null {
  const v = localStorage.getItem(KEY)
  if (!v) return null
  const n = Number(v)
  return Number.isFinite(n) ? n : null
}

export function setOwnerRestaurantId(id: number) {
  localStorage.setItem(KEY, String(id))
}
