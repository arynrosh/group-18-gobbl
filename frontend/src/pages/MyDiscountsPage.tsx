import { useEffect, useState } from 'react'
import { toast } from 'sonner'
import { useAuthStore, hasRole } from '../store/authStore'
import { getMyDiscountCodes } from '../features/discounts/discountApi'
import type { DiscountResponse } from '../types'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { StatusPill } from '../components/ui/StatusPill'

export function MyDiscountsPage() {
  const user = useAuthStore((s) => s.user)
  const [codes, setCodes] = useState<DiscountResponse[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!user || !hasRole(user, ['customer'])) return
    let cancelled = false
    ;(async () => {
      try {
        const data = await getMyDiscountCodes()
        if (!cancelled) setCodes(data)
      } catch (e) {
        if (!cancelled) toast.error(getApiErrorMessage(e))
      } finally {
        if (!cancelled) setLoading(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [user])

  if (!user || !hasRole(user, ['customer'])) {
    return <p className="text-gobbl-ink/75">Customers only.</p>
  }

  return (
    <div className="space-y-6">
      <h1 className="font-display text-4xl font-extrabold text-gobbl-ink">My promo codes</h1>
      <p className="text-sm text-gobbl-ink/65">Source: GET /discounts/my-codes</p>
      {loading ? (
        <p>Loading…</p>
      ) : codes.length === 0 ? (
        <Card>
          <p className="text-gobbl-ink/75">No codes assigned — check with an admin.</p>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {codes.map((c) => (
            <Card key={c.code_id} hoverLift>
              <div className="flex flex-wrap items-center gap-2">
                <StatusPill variant="success">{c.code}</StatusPill>
                <StatusPill variant="warning">{c.percentage}% off</StatusPill>
              </div>
              <p className="mt-3 text-sm text-gobbl-ink/70">Expires {c.expiry}</p>
              <p className="mt-2 text-xs text-gobbl-ink/55">
                assigned_to: {c.assigned_to.join(', ')} · used_by: {c.used_by.join(', ') || '—'}
              </p>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
