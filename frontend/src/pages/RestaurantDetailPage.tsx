import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { toast } from 'sonner'
import { fetchMenu, searchMenuByName } from '../features/restaurants/restaurantApi'
import {
  createOrder,
  addOrderItem,
  fetchOrder,
} from '../features/orders/orderApi'
import { getRestaurantAverageRating, getRestaurantReviews } from '../features/reviews/reviewApi'
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

export function RestaurantDetailPage() {
  const { id } = useParams()
  const restaurantId = Number(id)
  const navigate = useNavigate()
  const user = useAuthStore((s) => s.user)
  const { orderId, restaurantId: cartRid, setSession, clear } = useCartStore()

  const [menu, setMenu] = useState<MenuItem[]>([])
  const [loadingMenu, setLoadingMenu] = useState(true)
  const [avg, setAvg] = useState<number | null>(null)
  const [reviews, setReviews] = useState<unknown[]>([])
  const [priceTier, setPriceTier] = useState<string>('')
  const [minRating, setMinRating] = useState<string>('')
  const [menuNameQ, setMenuNameQ] = useState('')
  const debouncedMenuName = useDebouncedValue(menuNameQ, 300)
  const [globalMenuHits, setGlobalMenuHits] = useState<MenuItem[]>([])
  const [pendingItem, setPendingItem] = useState<MenuItem | null>(null)

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
          setAvg(typeof av.average_rating === 'number' ? av.average_rating : null)
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

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <div>
          <Link to="/restaurants" className="text-sm font-bold text-gobbl-teal hover:underline">
            ← All restaurants
          </Link>
          <h1 className="font-display mt-2 text-4xl font-extrabold text-gobbl-ink">{restaurantName}</h1>
          <div className="mt-2 flex flex-wrap items-center gap-2">
            <StatusPill variant="info">{menu[0]?.cuisine ?? 'Cuisine'}</StatusPill>
            {avg !== null && (
              <StatusPill variant="success">Avg rating {avg.toFixed(2)}</StatusPill>
            )}
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link to="/cart">
            <Button variant="mint">View cart</Button>
          </Link>
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
        <h2 className="font-display text-xl font-bold text-gobbl-ink">Reviews snapshot</h2>
        {reviews.length === 0 ? (
          <p className="mt-2 text-gobbl-ink/70">No reviews yet for this spot.</p>
        ) : (
          <ul className="mt-3 space-y-2 text-sm text-gobbl-ink/80">
            {reviews.slice(0, 5).map((r, idx) => (
              <li key={idx} className="rounded-2xl bg-white/60 px-3 py-2 font-mono text-xs">
                {JSON.stringify(r)}
              </li>
            ))}
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
