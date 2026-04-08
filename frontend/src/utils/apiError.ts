import axios from 'axios'

export function getApiErrorMessage(err: unknown, fallback = 'Something went wrong'): string {
  if (!axios.isAxiosError(err)) {
    return err instanceof Error ? err.message : fallback
  }
  const data = err.response?.data as { detail?: unknown } | undefined
  const detail = data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    const parts = detail.map((d) => {
      if (typeof d === 'object' && d !== null && 'msg' in d) return String((d as { msg: string }).msg)
      return JSON.stringify(d)
    })
    return parts.join('; ') || fallback
  }
  if (detail && typeof detail === 'object') return JSON.stringify(detail)
  if (err.message) return err.message
  return fallback
}
