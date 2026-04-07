import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { toast } from 'sonner'
import { useAuthStore, hasRole } from '../store/authStore'
import { getReviewableItems, submitReview } from '../features/reviews/reviewApi'
import type { ItemRatingInput, ReviewableItem } from '../types'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input, Label } from '../components/ui/Input'

export function ReviewOrderPage() {
  const { orderId } = useParams()
  const user = useAuthStore((s) => s.user)
  const [items, setItems] = useState<ReviewableItem[]>([])
  const [ratings, setRatings] = useState<Record<number, number>>({})
  const [writtenReviews, setWrittenReviews] = useState<Record<number, string>>({})
  const [food_temperature, setFoodTemperature] = useState('hot')
  const [food_freshness, setFoodFreshness] = useState(5)
  const [packaging_quality, setPackagingQuality] = useState(5)
  const [food_condition, setFoodCondition] = useState('great')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    if (!orderId) return
    let cancelled = false
    ;(async () => {
      try {
        const res = await getReviewableItems(orderId)
        if (!cancelled) {
          setItems(res.items)
          const init: Record<number, number> = {}
          const initWritten: Record<number, string> = {}
          res.items.forEach((i) => {
            init[i.menu_item_id] = 5
            initWritten[i.menu_item_id] = i.written_review ?? ''
          })
          setRatings(init)
          setWrittenReviews(initWritten)
        }
      } catch (e) {
        if (!cancelled) toast.error(getApiErrorMessage(e))
      }
    })()
    return () => {
      cancelled = true
    }
  }, [orderId])

  if (!user || !hasRole(user, ['customer'])) {
    return <p className="text-gobbl-ink/75">Customers only.</p>
  }

  if (!orderId) return null

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <h1 className="font-display text-3xl font-extrabold text-gobbl-ink">Review order</h1>
      <Card>
        <h2 className="font-display text-lg font-bold">Item ratings</h2>
        <p className="text-xs text-gobbl-ink/60">POST /reviews/ with item_ratings matching backend schema.</p>
        <ul className="mt-4 space-y-4">
          {items.map((it) => (
            <li key={it.menu_item_id} className="rounded-2xl bg-white/70 px-4 py-3">
              <p className="font-bold">{it.food_item}</p>
              <Label htmlFor={`r-${it.menu_item_id}`}>customer_rating (1-5)</Label>
              <Input
                id={`r-${it.menu_item_id}`}
                type="number"
                min={1}
                max={5}
                value={ratings[it.menu_item_id] ?? 5}
                onChange={(e) =>
                  setRatings((r) => ({ ...r, [it.menu_item_id]: Number(e.target.value) }))
                }
              />
              <Label htmlFor={`w-${it.menu_item_id}`}>written_review (optional)</Label>
              <Input
                id={`w-${it.menu_item_id}`}
                value={writtenReviews[it.menu_item_id] ?? ''}
                onChange={(e) =>
                  setWrittenReviews((r) => ({ ...r, [it.menu_item_id]: e.target.value }))
                }
                placeholder="How was this specific item?"
              />
            </li>
          ))}
        </ul>
      </Card>
      <Card>
        <h2 className="font-display text-lg font-bold">Overall experience</h2>
        <div className="mt-4 grid gap-4">
          <div>
            <Label htmlFor="ft">food_temperature</Label>
            <Input id="ft" value={food_temperature} onChange={(e) => setFoodTemperature(e.target.value)} required />
          </div>
          <div>
            <Label htmlFor="ff">food_freshness (1-5)</Label>
            <Input
              id="ff"
              type="number"
              min={1}
              max={5}
              value={food_freshness}
              onChange={(e) => setFoodFreshness(Number(e.target.value))}
            />
          </div>
          <div>
            <Label htmlFor="pq">packaging_quality (1-5)</Label>
            <Input
              id="pq"
              type="number"
              min={1}
              max={5}
              value={packaging_quality}
              onChange={(e) => setPackagingQuality(Number(e.target.value))}
            />
          </div>
          <div>
            <Label htmlFor="fc">food_condition</Label>
            <Input id="fc" value={food_condition} onChange={(e) => setFoodCondition(e.target.value)} required />
          </div>
        </div>
        <Button
          className="mt-6 w-full"
          disabled={busy || items.length === 0}
          onClick={async () => {
            setBusy(true)
            try {
              const item_ratings: ItemRatingInput[] = items.map((it) => ({
                menu_item_id: it.menu_item_id,
                food_item: it.food_item,
                customer_rating: ratings[it.menu_item_id] ?? 5,
                written_review: (writtenReviews[it.menu_item_id] ?? '').trim() || null,
              }))
              await submitReview({
                order_id: orderId,
                food_temperature,
                food_freshness,
                packaging_quality,
                food_condition,
                item_ratings,
              })
              toast.success('Review submitted!')
            } catch (e) {
              toast.error(getApiErrorMessage(e))
            } finally {
              setBusy(false)
            }
          }}
        >
          Submit review
        </Button>
      </Card>
    </div>
  )
}
