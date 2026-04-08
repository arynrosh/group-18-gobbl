import { useState } from 'react'
import { toast } from 'sonner'
import { useAuthStore, hasRole } from '../store/authStore'
import { addDietRestriction, removeDietRestriction } from '../features/diet-restrictions/dietRestrictionsApi'
import type { DietRestrictionsEntry } from '../types'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'

const COMMON = ['Vegan', 'Vegetarian', 'Gluten-Free', 'Lactose Intolerance', 'Nut Allergy']

export function DietRestrictionsPage() {
  const user = useAuthStore((s) => s.user)
  const [entry, setEntry] = useState<DietRestrictionsEntry | null>(null)
  const [input, setInput] = useState('')
  const [busy, setBusy] = useState(false)

  if (!user || !hasRole(user, ['customer'])) {
    return <p className="text-gobbl-ink/75">Customers only.</p>
  }

  async function onAdd(v: string) {
    const value = v.trim()
    if (!value) return
    setBusy(true)
    try {
      const data = await addDietRestriction(user.username, value)
      setEntry(data)
      setInput('')
      toast.success('Restriction saved')
    } catch (e) {
      toast.error(getApiErrorMessage(e))
    } finally {
      setBusy(false)
    }
  }

  async function onRemove(v: string) {
    setBusy(true)
    try {
      const data = await removeDietRestriction(user.username, v)
      setEntry(data)
      toast.success('Restriction removed')
    } catch (e) {
      toast.error(getApiErrorMessage(e))
    } finally {
      setBusy(false)
    }
  }

  const items = entry?.diet_restrictions ?? []

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <h1 className="font-display text-4xl font-extrabold text-gobbl-ink">Diet restrictions</h1>
      <Card>
        <p className="text-sm text-gobbl-ink/70">
          Backend endpoints: <code className="rounded bg-white/80 px-1">POST /diet_restrictions/{'{username}'}/diet_restrictions?diet_restriction=...</code> and{' '}
          <code className="rounded bg-white/80 px-1">DELETE /diet_restrictions/{'{username}'}/diet_restrictions/{'{diet_restriction}'}</code>.
        </p>
        <p className="mt-2 text-xs text-gobbl-ink/60">
          Backend currently has no dedicated GET route for restrictions; list below reflects the latest mutation response.
        </p>
      </Card>

      <Card>
        <h2 className="font-display text-lg font-bold">Quick add</h2>
        <div className="mt-3 flex flex-wrap gap-2">
          {COMMON.map((c) => (
            <Button key={c} variant="secondary" className="!py-2 !text-sm" disabled={busy} onClick={() => void onAdd(c)}>
              + {c}
            </Button>
          ))}
        </div>
        <div className="mt-4 flex gap-2">
          <Input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Add custom restriction" />
          <Button disabled={busy || !input.trim()} onClick={() => void onAdd(input)}>
            Add
          </Button>
        </div>
      </Card>

      <Card>
        <h2 className="font-display text-lg font-bold">Current restrictions</h2>
        {items.length === 0 ? (
          <p className="mt-3 text-sm text-gobbl-ink/70">No restrictions loaded yet. Add one above to initialize your profile entry.</p>
        ) : (
          <ul className="mt-3 space-y-2">
            {items.map((r) => (
              <li key={r} className="flex items-center justify-between gap-3 rounded-2xl bg-white/70 px-4 py-2">
                <span className="font-semibold">{r}</span>
                <Button variant="ghost" className="!py-1 !text-sm" disabled={busy} onClick={() => void onRemove(r)}>
                  Remove
                </Button>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  )
}
