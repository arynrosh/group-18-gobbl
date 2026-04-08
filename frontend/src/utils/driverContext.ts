const KEY = 'gobbl_driver_id'

export function getDriverId(): number | null {
  const v = localStorage.getItem(KEY)
  if (!v) return null
  const n = Number(v)
  return Number.isFinite(n) ? n : null
}

export function setDriverId(id: number) {
  localStorage.setItem(KEY, String(id))
}
