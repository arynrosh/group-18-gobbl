import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { toast } from 'sonner'
import { useAuthStore, hasRole } from '../store/authStore'
import { getRecommendations } from '../features/recommendations/recommendationApi'
import type { RecommendedItem } from '../types'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'

export function RecommendationsPage() {
  const user = useAuthStore((s) => s.user)
  const [items, setItems] = useState<RecommendedItem[] | null>(null)

  useEffect(() => {
    if (!user || !hasRole(user, ['customer'])) return
    let cancelled = false
    ;(async () => {
      try {
        const data = await getRecommendations(user.username, 12)
        if (!cancelled) setItems(data)
      } catch (e) {
        const msg = getApiErrorMessage(e, '')
        if (!cancelled) {
          setItems([])
          if (!msg.toLowerCase().includes('404')) toast.error(msg)
        }
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
      <h1 className="font-display text-4xl font-extrabold text-gobbl-ink">Recommendations</h1>
      <p className="text-sm text-gobbl-ink/65">
        GET /recommendations/{'{customer_id}'} — backend 404 means “no history yet” (we show a friendly empty state).
      </p>
      {items === null ? (
        <p>Loading…</p>
      ) : items.length === 0 ? (
        <Card>
          <p className="text-lg font-semibold">No recommendations yet</p>
          <p className="mt-2 text-sm text-gobbl-ink/70">Order something first — the API needs past orders to suggest items.</p>
          <Link to="/restaurants">
            <Button className="mt-4">Browse restaurants</Button>
          </Link>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {items.map((r) => (
            <Card key={`${r.menu_item_id}-${r.restaurant_id}`} hoverLift>
              <p className="font-display text-xl font-bold">{r.food_item}</p>
              <p className="text-sm text-gobbl-ink/70">{r.restaurant_name}</p>
              <p className="mt-2 text-xs font-bold uppercase text-gobbl-teal">{r.cuisine}</p>
              <p className="mt-3 text-lg font-black text-gobbl-tomato">${r.order_value.toFixed(2)}</p>
              <Link to={`/restaurants/${r.restaurant_id}`}>
                <Button className="mt-4 w-full !py-2 !text-sm" variant="mint">
                  Open restaurant
                </Button>
              </Link>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
