import { api } from '../../api/client'
import type { RecommendedItem } from '../../types'

/** Backend returns 404 when there is no history — callers should treat as empty. */
export async function getRecommendations(customerId: string, limit = 8): Promise<RecommendedItem[]> {
  const { data } = await api.get<RecommendedItem[]>(`/recommendations/${encodeURIComponent(customerId)}`, {
    params: { limit },
  })
  return data
}
