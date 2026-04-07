import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { toast } from 'sonner'
import { fetchMenu, searchMenuByName } from '../features/restaurants/restaurantApi'
import {
  createOrder,
  addOrderItem,
  fetchOrder,
  addMysteryBag,
} from '../features/orders/orderApi'
import { getRestaurantAverageRating, getRestaurantReviews, type RestaurantReview } from '../features/reviews/reviewApi'
import { useCartStore } from '../store/cartStore'
import { useAuthStore, hasRole } from '../store/authStore'
import type { MenuItem } from '../types'
import { getApiErrorMessage } from '../utils/apiError'
import { useDebouncedValue } from '../hooks/useDebouncedValue'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input, Label } from '../components/ui/Input'
import { StatusPill } from '../components/ui/StatusPill'
import { Skeleton } from '../components/ui/Skeleton'
import { ConfirmDialog } from '../components/ConfirmDialog'

const TIERS = ['$', '$$', '$$$', '$$$$'] as const

function starsExact(n: number) {
  return '★'.repeat(Math.max(0, Math.min(5, Math.round(Number(n)))))
}

export function RestaurantDetailPage() {
  const { id } = useParams()
  const restaurantId = Number(id)
  const navigate = useNavigate()
  const user = useAuthStore((s) => s.user)
  const { orderId, restaurantId: cartRid, setSession, clear } = useCartStore()

  const [menu, setMenu] = useState<MenuItem[]>([])
  const [loadingMenu, setLoadingMenu] = useState(true)
  const [avg, setAvg] = useState<number | null>(null)
  const [reviews, setReviews] = useState<RestaurantReview[]>([])
  const [priceTier, setPriceTier] = useState<string>('')
  const [minRating, setMinRating] = useState<string>('')
  const [menuNameQ, setMenuNameQ] = useState('')
  const debouncedMenuName = useDebouncedValue(menuNameQ, 300)
  const [globalMenuHits, setGlobalMenuHits] = useState<MenuItem[]>([])
  const [pendingItem, setPendingItem] = useState<MenuItem | null>(null)
  const [mysteryBudget, setMysteryBudget] = useState('20')
  const [mysteryBusy, setMysteryBusy] = useState(false)

  const restaurantName = menu[0]?.restaurant_name ?? `Restaurant #${restaurantId}`

  useEffect(() => {
    if (!Number.isFinite(restaurantId)) return
    let cancelled = false
    ;(async () => {
      setLoadingMenu(true)
      try {
        const [m, av, rev] = await Promise.all([
          fetchMenu(restaurantId, {
            price_tier: priceTier || undefined,
            min_rating: minRating ? Number(minRating) : undefined,
          }),
          getRestaurantAverageRating(restaurantId).catch(() => ({ average_rating: 0 })),
          getRestaurantReviews(restaurantId).catch(() => []),
        ])
        if (!cancelled) {
          setMenu(m)
          const raw = av.average_rating
          const n = typeof raw === 'number' ? raw : Number(raw)
          setAvg(Number.isFinite(n) ? n : null)
          setReviews(Array.isArray(rev) ? rev : [])
        }
      } catch (e) {
        if (!cancelled) toast.error(getApiErrorMessage(e))
      } finally {
        if (!cancelled) setLoadingMenu(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [restaurantId, priceTier, minRating])

  useEffect(() => {
    if (!debouncedMenuName.trim()) {
      setGlobalMenuHits([])
      return
    }
    let cancelled = false
    ;(async () => {
      try {
        const res = await searchMenuByName(debouncedMenuName.trim(), 30, 0)
        const local = (res.items as MenuItem[]).filter((i) => i.restaurant_id === restaurantId)
        if (!cancelled) setGlobalMenuHits(local)
      } catch {
        if (!cancelled) setGlobalMenuHits([])
      }
    })()
    return () => {
      cancelled = true
    }
  }, [debouncedMenuName, restaurantId])

  const visibleMenu = useMemo(() => {
    if (!debouncedMenuName.trim()) return menu
    const q = debouncedMenuName.toLowerCase()
    const base = globalMenuHits.length ? globalMenuHits : menu
    return base.filter((i) => i.food_item.toLowerCase().includes(q))
  }, [menu, globalMenuHits, debouncedMenuName])

  async function createFreshOrder(): Promise<string | null> {
    if (!user || !hasRole(user, ['customer'])) {
      toast.error('Log in as a customer to order.')
      navigate('/login', { state: { from: `/restaurants/${restaurantId}` } })
      return null
    }
    const newId = crypto.randomUUID()
    try {
      const o = await createOrder({
        order_id: newId,
        restaurant_id: restaurantId,
        delivery_distance: useCartStore.getState().deliveryDistance,
        delivery_time: useCartStore.getState().deliveryTime,
      })
      setSession({
        orderId: o.order_id,
        restaurantId: o.restaurant_id,
        deliveryDistance: o.delivery_distance,
        deliveryTime: o.delivery_time,
      })
      toast.success('Started a new order!')
      return o.order_id
    } catch (e) {
      toast.error(getApiErrorMessage(e))
      return null
    }
  }

  async function addItem(item: MenuItem) {
    if (!user || !hasRole(user, ['customer'])) {
      toast.error('Log in as a customer to order.')
      navigate('/login', { state: { from: `/restaurants/${restaurantId}` } })
      return
    }
    if (orderId && cartRid !== null && cartRid !== restaurantId) {
      setPendingItem(item)
      return
    }
    await performAdd(item)
  }

  async function performAdd(item: MenuItem) {
    const { orderId: oidNow, restaurantId: ridNow } = useCartStore.getState()
    let oid = oidNow
    if (!oid || ridNow !== restaurantId) {
      oid = await createFreshOrder()
      if (!oid) return
    }
    try {
      await addOrderItem({
        orderId: oid,
        restaurant_id: restaurantId,
        food_item: item.food_item,
        quantity: 1,
      })
      const fresh = await fetchOrder(oid)
      useCartStore.getState().setSession({
        orderId: fresh.order_id,
        restaurantId: fresh.restaurant_id,
        deliveryDistance: fresh.delivery_distance,
        deliveryTime: fresh.delivery_time,
      })
      toast.success(`Added ${item.food_item}`)
    } catch (e) {
      toast.error(getApiErrorMessage(e))
    }
  }

  async function handleMysteryBag() {
    if (!user || !hasRole(user, ['customer'])) {
      toast.error('Log in as a customer to order.')
      navigate('/login', { state: { from: `/restaurants/${restaurantId}` } })
      return
    }
    const b = Number(mysteryBudget)
    if (!Number.isFinite(b) || b <= 0) {
      toast.error('Enter a valid mystery budget.')
      return
    }
    setMysteryBusy(true)
    try {
      let oid = useCartStore.getState().orderId
      const ridNow = useCartStore.getState().restaurantId
      if (oid && ridNow !== null && ridNow !== restaurantId) {
        toast.error('You have a cart for a different restaurant. Clear it first.')
        return
      }
      if (!oid || ridNow !== restaurantId) {
        oid = await createFreshOrder()
        if (!oid) return
      }
      await addMysteryBag(oid, b)
      await fetchOrder(oid)
      toast.success('Mystery bag added to your order!')
      navigate('/cart')
    } catch (e) {
      toast.error(getApiErrorMessage(e))
    } finally {
      setMysteryBusy(false)
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <Link to="/restaurants" className="text-sm font-bold text-gobbl-teal hover:underline">
          ← All restaurants
        </Link>
        <div className="mt-2 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between sm:gap-6">
          <div className="flex min-w-0 flex-1 flex-wrap items-center gap-x-4 gap-y-2">
            <h1 className="min-w-0 flex-1 font-display text-4xl font-extrabold leading-tight text-gobbl-ink">
              {restaurantName}
            </h1>
            {avg !== null && (
              <div
                className="flex shrink-0 items-center gap-2"
                title={`Restaurant average: ${avg.toFixed(2)} out of 5`}
              >
                <span className="text-[10px] font-bold uppercase tracking-wide text-gobbl-ink/45">Rating</span>
                <span className="font-display text-xl leading-none tracking-tight text-gobbl-mango">
                  {starsExact(Math.round(avg))}
                </span>
              </div>
            )}
          </div>
          <div className="shrink-0">
            <Link to="/cart">
              <Button variant="mint">View cart</Button>
            </Link>
          </div>
        </div>
        <div className="mt-2 flex flex-wrap items-center gap-2">
          <StatusPill variant="info">{menu[0]?.cuisine ?? 'Cuisine'}</StatusPill>
        </div>
      </div>

      <Card>
        <h2 className="font-display text-xl font-bold text-gobbl-ink">Menu search & filters</h2>
        <p className="mt-1 text-sm text-gobbl-ink/65">
          Name search uses <code className="rounded bg-white/80 px-1">GET /menu/search/name</code> then filters to this restaurant.
          Tier & rating use <code className="rounded bg-white/80 px-1">GET /menu/:id</code> query params.
        </p>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          <div>
            <Label htmlFor="mn">Menu item name</Label>
            <Input id="mn" value={menuNameQ} onChange={(e) => setMenuNameQ(e.target.value)} placeholder="Crispy, spicy, etc." />
          </div>
          <div>
            <Label htmlFor="pt">Price tier</Label>
            <select
              id="pt"
              className="w-full rounded-2xl border-2 border-gobbl-peach/80 bg-white/90 px-4 py-3 font-semibold"
              value={priceTier}
              onChange={(e) => setPriceTier(e.target.value)}
            >
              <option value="">Any</option>
              {TIERS.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </div>
          <div>
            <Label htmlFor="mr">Minimum rating</Label>
            <Input
              id="mr"
              type="number"
              step="0.1"
              min={0}
              max={5}
              value={minRating}
              onChange={(e) => setMinRating(e.target.value)}
              placeholder="e.g. 4"
            />
          </div>
        </div>
      </Card>

      <Card className="border-2 border-dashed border-gobbl-mango/70 bg-gradient-to-br from-gobbl-lemon/25 to-gobbl-mango/20">
        <h2 className="font-display text-xl font-extrabold text-gobbl-ink">Mystery bag for this restaurant ✨</h2>
        <p className="mt-1 text-sm text-gobbl-ink/70">
          Build a surprise combo from this menu using <code className="rounded bg-white/70 px-1">POST /orders/:id/mystery-bag</code>.
        </p>
        <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-end">
          <div className="min-w-[180px] flex-1">
            <Label htmlFor="mystery-budget">Budget</Label>
            <Input
              id="mystery-budget"
              type="number"
              min="0.01"
              step="0.01"
              value={mysteryBudget}
              onChange={(e) => setMysteryBudget(e.target.value)}
            />
          </div>
          <Button disabled={mysteryBusy} onClick={() => void handleMysteryBag()}>
            {mysteryBusy ? 'Adding…' : 'Add mystery bag'}
          </Button>
        </div>
      </Card>

      {loadingMenu ? (
        <div className="grid gap-4 md:grid-cols-2">
          <Skeleton className="h-36" />
          <Skeleton className="h-36" />
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {visibleMenu.map((item) => (
            <Card key={item.menu_item_id} hoverLift>
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h3 className="font-display text-xl font-bold text-gobbl-ink">{item.food_item}</h3>
                  <p className="text-sm text-gobbl-ink/65">{item.cuisine}</p>
                  <div className="mt-2 flex flex-wrap gap-2">
                    {item.customer_rating != null && (
                      <StatusPill variant="warning">★ {item.customer_rating.toFixed(1)}</StatusPill>
                    )}
                  </div>
                </div>
                <p className="text-xl font-black text-gobbl-tomato">${item.order_value.toFixed(2)}</p>
              </div>
              <Button className="mt-4 w-full !py-2" onClick={() => void addItem(item)}>
                Add to order
              </Button>
            </Card>
          ))}
        </div>
      )}

      <Card>
        <h2 className="font-display text-xl font-bold text-gobbl-ink">Reviews</h2>
        {reviews.length === 0 ? (
          <p className="mt-2 text-sm text-gobbl-ink/65">No reviews yet for this spot.</p>
        ) : (
          <ul className="mt-5 space-y-4">
            {reviews.slice(0, 5).map((r) => {
              const foodLabels = r.item_ratings.map((it) => it.food_item).join(' · ')
              const multi = r.item_ratings.length > 1
              const avgRating =
                r.item_ratings.length > 0
                  ? r.item_ratings.reduce((sum, it) => sum + it.customer_rating, 0) / r.item_ratings.length
                  : 0
              const overallStars = starsExact(Math.round(avgRating))
              const topWritten = r.item_ratings.find((it) => !!it.written_review)?.written_review
              return (
                <li
                  key={r.review_id}
                  className="overflow-hidden rounded-2xl border border-gobbl-peach/50 bg-white/90 shadow-[0_2px_12px_-4px_rgba(45,42,50,0.12)]"
                >
                  <div className="border-b border-gobbl-peach/30 bg-gradient-to-r from-gobbl-cream/90 to-white px-4 py-3.5">
                    <div className="flex flex-wrap items-start justify-between gap-3">
                      <div className="flex min-w-0 flex-1 flex-wrap items-center gap-x-2 gap-y-1 sm:gap-x-3">
                        <div className="flex min-w-0 max-w-full items-center gap-x-2">
                          <span className="shrink-0 text-[10px] font-bold uppercase tracking-wide text-gobbl-ink/45">
                            Customer
                          </span>
                          <span className="min-w-0 truncate text-sm leading-snug text-gobbl-ink/75">{r.customer_id}</span>
                        </div>
                        <span className="shrink-0 select-none text-gobbl-ink/25" aria-hidden>
                          ·
                        </span>
                        <div className="flex min-w-0 max-w-full flex-1 items-center gap-x-2">
                          <span className="shrink-0 text-[10px] font-bold uppercase tracking-wide text-gobbl-ink/45">
                            Food
                          </span>
                          <span className="min-w-0 break-words text-sm leading-snug text-gobbl-ink/75">{foodLabels}</span>
                        </div>
                      </div>
                      <div className="shrink-0 text-right">
                        <p className="text-[10px] font-bold uppercase tracking-wide text-gobbl-ink/45">
                          Overall
                        </p>
                        <p
                          className="mt-0.5 font-display text-xl leading-none tracking-tight text-gobbl-mango"
                          title={`${avgRating.toFixed(1)} average (out of 5)`}
                        >
                          {overallStars || '—'}
                        </p>
                      </div>
                    </div>
                    <div className="mt-3 grid grid-cols-1 gap-2 sm:grid-cols-2">
                      <div className="rounded-xl border border-gobbl-peach/35 bg-white/60 px-3 py-2">
                        <p className="text-[10px] font-bold uppercase tracking-wide text-gobbl-ink/45">
                          Food temperature
                        </p>
                        <p className="mt-0.5 text-sm leading-snug text-gobbl-ink/85">{r.food_temperature}</p>
                      </div>
                      <div className="rounded-xl border border-gobbl-peach/35 bg-white/60 px-3 py-2">
                        <p className="text-[10px] font-bold uppercase tracking-wide text-gobbl-ink/45">
                          Food condition
                        </p>
                        <p className="mt-0.5 text-sm leading-snug text-gobbl-ink/85">{r.food_condition}</p>
                      </div>
                      <div className="rounded-xl border border-gobbl-peach/35 bg-white/60 px-3 py-2">
                        <p className="text-[10px] font-bold uppercase tracking-wide text-gobbl-ink/45">
                          Freshness
                        </p>
                        <p
                          className="mt-0.5 font-display text-sm tracking-tight text-gobbl-mango"
                          title={`${r.food_freshness} out of 5`}
                        >
                          {starsExact(r.food_freshness)}
                        </p>
                      </div>
                      <div className="rounded-xl border border-gobbl-peach/35 bg-white/60 px-3 py-2">
                        <p className="text-[10px] font-bold uppercase tracking-wide text-gobbl-ink/45">
                          Packaging
                        </p>
                        <p
                          className="mt-0.5 font-display text-sm tracking-tight text-gobbl-mango"
                          title={`${r.packaging_quality} out of 5`}
                        >
                          {starsExact(r.packaging_quality)}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="divide-y divide-gobbl-peach/25">
                    {topWritten && (
                      <div className="px-4 py-3.5">
                        <blockquote className="border-l-2 border-gobbl-mango/60 pl-3 text-sm leading-relaxed text-gobbl-ink/80">
                          {topWritten}
                        </blockquote>
                      </div>
                    )}
                    {r.item_ratings.map((it) => (
                      (multi || (it.written_review && it.written_review !== topWritten)) && (
                        <div key={`${r.review_id}-${it.menu_item_id}`} className="px-4 py-3.5">
                          {multi && <span className="text-sm font-semibold text-gobbl-ink">{it.food_item}</span>}
                          {it.written_review && it.written_review !== topWritten && (
                            <blockquote className="mt-2 border-l-2 border-gobbl-mango/60 pl-3 text-sm leading-relaxed text-gobbl-ink/80">
                              {it.written_review}
                            </blockquote>
                          )}
                        </div>
                      )
                    ))}
                  </div>
                </li>
              )
            })}
          </ul>
        )}
      </Card>

      <ConfirmDialog
        open={!!pendingItem}
        title="Start a new cart?"
        message="You already have items for another restaurant. Clear the current cart and start fresh here?"
        onClose={() => setPendingItem(null)}
        onConfirm={() => {
          const item = pendingItem
          clear()
          setPendingItem(null)
          if (item) void performAdd(item)
        }}
        danger
        confirmLabel="Clear & continue"
      />
    </div>
  )
}
