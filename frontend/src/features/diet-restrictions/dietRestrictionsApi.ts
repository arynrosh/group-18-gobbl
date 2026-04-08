import { api } from '../../api/client'
import type { DietRestrictionsEntry } from '../../types'

const BASE = '/diet_restrictions'

export async function addDietRestriction(username: string, diet_restriction: string): Promise<DietRestrictionsEntry> {
  const { data } = await api.post<DietRestrictionsEntry>(
    `${BASE}/${encodeURIComponent(username)}/diet_restrictions`,
    null,
    { params: { diet_restriction } },
  )
  return data
}

export async function removeDietRestriction(username: string, diet_restriction: string): Promise<DietRestrictionsEntry> {
  const { data } = await api.delete<DietRestrictionsEntry>(
    `${BASE}/${encodeURIComponent(username)}/diet_restrictions/${encodeURIComponent(diet_restriction)}`,
  )
  return data
}
