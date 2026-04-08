import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { toast } from 'sonner'
import {
  browseRestaurants,
  searchRestaurantsByName,
  searchRestaurantsByCuisine,
} from '../features/restaurants/restaurantApi'
import {
  fetchRestaurantsRankedByAggregatedReviewRatings,
  fetchRestaurantsRankedByOrders,
} from '../features/restaurants/popularRestaurants'
import type { Restaurant } from '../types'
import { getRestaurantAverageRating } from '../features/reviews/reviewApi'
import { getApiErrorMessage } from '../utils/apiError'
import { useDebouncedValue } from '../hooks/useDebouncedValue'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input, Label } from '../components/ui/Input'
import { Skeleton } from '../components/ui/Skeleton'
import { StatusPill } from '../components/ui/StatusPill'

const PAGE = 12

function starsExact(n: number) {
  return '★'.repeat(Math.max(0, Math.min(5, Math.round(Number(n)))))
}

export function RestaurantsPage() {
  const [mode, setMode] = useState<
    'browse' | 'name' | 'cuisine' | 'popular_orders' | 'popular_ratings'
  >('browse')
  const [nameQ, setNameQ] = useState('')
  const [cuisineQ, setCuisineQ] = useState('')
  const debouncedName = useDebouncedValue(nameQ, 350)
  const debouncedCuisine = useDebouncedValue(cuisineQ, 350)

  const [items, setItems] = useState<Restaurant[]>([])
  const [total, setTotal] = useState(0)
  const [offset, setOffset] = useState(0)
  const [loading, setLoading] = useState(true)
  const [avgByRestaurant, setAvgByRestaurant] = useState<Record<number, number>>({})
  const [rankedList, setRankedList] = useState<Restaurant[] | null>(null)
  const [orderCountById, setOrderCountById] = useState<Record<number, number>>({})

  const load = useCallback(async () => {
    if (mode === 'popular_orders' || mode === 'popular_ratings') return
    setLoading(true)
    setRankedList(null)
    try {
      let res
      if (mode === 'name' && debouncedName.trim()) {
        res = await searchRestaurantsByName(debouncedName.trim(), PAGE, offset)
      } else if (mode === 'cuisine' && debouncedCuisine.trim()) {
        res = await searchRestaurantsByCuisine(debouncedCuisine.trim(), PAGE, offset)
      } else {
        res = await browseRestaurants(PAGE, offset)
      }
      setItems(res.items as Restaurant[])
      setTotal(res.total)
    } catch (e) {
      toast.error(getApiErrorMessage(e))
    } finally {
      setLoading(false)
    }
  }, [mode, debouncedName, debouncedCuisine, offset])

  useEffect(() => {
    void load()
  }, [load])

  useEffect(() => {
    setOffset(0)
  }, [mode, debouncedName, debouncedCuisine])

  useEffect(() => {
    if (mode !== 'popular_orders' && mode !== 'popular_ratings') return
    let cancelled = false
    setLoading(true)
    setRankedList(null)
    ;(async () => {
      try {
        if (mode === 'popular_orders') {
          const { restaurants, orderCountById: counts } = await fetchRestaurantsRankedByOrders(150)
          if (cancelled) return
          setOrderCountById(counts)
          setAvgByRestaurant({})
          setRankedList(restaurants)
          setTotal(restaurants.length)
        } else {
          const { restaurants, ratingById } = await fetchRestaurantsRankedByAggregatedReviewRatings(200, 150)
          if (cancelled) return
          setOrderCountById({})
          setAvgByRestaurant(ratingById)
          setRankedList(restaurants)
          setTotal(restaurants.length)
        }
      } catch (e) {
        if (!cancelled) toast.error(getApiErrorMessage(e))
      } finally {
        if (!cancelled) setLoading(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [mode])

  useEffect(() => {
    if (rankedList === null) return
    setItems(rankedList.slice(offset, offset + PAGE))
  }, [rankedList, offset])

  useEffect(() => {
    if (mode === 'popular_ratings') return
    if (!items.length) {
      if (mode !== 'popular_orders') setAvgByRestaurant({})
      return
    }
    let cancelled = false
    ;(async () => {
      const results = await Promise.all(
        items.map((r) =>
          getRestaurantAverageRating(r.restaurant_id)
            .then((av) => {
              const raw = av.average_rating
              const n = typeof raw === 'number' ? raw : Number(raw)
              return [r.restaurant_id, Number.isFinite(n) ? n : null] as const
            })
            .catch(() => [r.restaurant_id, null] as const),
        ),
      )
      if (cancelled) return
      const next: Record<number, number> = {}
      for (const [id, val] of results) {
        if (val != null) next[id] = val
      }
      setAvgByRestaurant(next)
    })()
    return () => {
      cancelled = true
    }
  }, [items, mode])

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-display text-4xl font-extrabold text-gobbl-ink">Restaurants</h1>
        <p className="mt-1 text-gobbl-ink/70">
          Browse, search, or sort by popularity — orders use{' '}
          <code className="rounded bg-gobbl-ink/[0.04] px-1 text-xs">/statistics/popular-restaurants/orders</code>
          ; top ratings rank by stars in submitted reviews (aggregated from{' '}
          <code className="rounded bg-gobbl-ink/[0.04] px-1 text-xs">/reviews/restaurant/:id</code>
          ).
        </p>
      </div>

      <Card className="flex flex-col gap-4 md:flex-row md:items-end">
        <div className="flex flex-wrap gap-2">
          <Button variant={mode === 'browse' ? 'primary' : 'secondary'} onClick={() => setMode('browse')}>
            All
          </Button>
          <Button variant={mode === 'name' ? 'primary' : 'secondary'} onClick={() => setMode('name')}>
            Search name
          </Button>
          <Button variant={mode === 'cuisine' ? 'primary' : 'secondary'} onClick={() => setMode('cuisine')}>
            Cuisine
          </Button>
          <Button
            variant={mode === 'popular_orders' ? 'primary' : 'secondary'}
            onClick={() => setMode('popular_orders')}
          >
            Popular by orders
          </Button>
          <Button
            variant={mode === 'popular_ratings' ? 'primary' : 'secondary'}
            onClick={() => setMode('popular_ratings')}
          >
            Popular by rating
          </Button>
        </div>
        {mode === 'name' && (
          <div className="min-w-[220px] flex-1">
            <Label htmlFor="nq">Restaurant name</Label>
            <Input id="nq" value={nameQ} onChange={(e) => setNameQ(e.target.value)} placeholder="e.g. Sushi" />
          </div>
        )}
        {mode === 'cuisine' && (
          <div className="min-w-[220px] flex-1">
            <Label htmlFor="cq">Cuisine contains</Label>
            <Input id="cq" value={cuisineQ} onChange={(e) => setCuisineQ(e.target.value)} placeholder="e.g. Italian" />
          </div>
        )}
      </Card>

      {loading ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-40" />
          ))}
        </div>
      ) : items.length === 0 ? (
        <Card>
          <p className="text-gobbl-ink/75">
            {mode === 'popular_orders'
              ? 'No restaurants with orders in the dataset yet — place some orders or browse all.'
              : mode === 'popular_ratings'
                ? 'No rated restaurants yet — reviews with item ratings will appear here.'
                : 'No restaurants match — try another search or browse all.'}
          </p>
        </Card>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((r) => (
            <Link key={r.restaurant_id} to={`/restaurants/${r.restaurant_id}`}>
              <Card hoverLift className="h-full !p-0 overflow-hidden">
                <div className="bg-gradient-to-br from-gobbl-mango/80 to-gobbl-tomato/80 p-5 text-white">
                  <div className="flex min-w-0 items-center gap-3">
                    <h2 className="min-w-0 flex-1 font-display text-2xl font-bold leading-tight drop-shadow-sm">
                      {r.restaurant_name}
                    </h2>
                    {avgByRestaurant[r.restaurant_id] != null && (
                      <div
                        className="flex shrink-0 items-center gap-1.5"
                        title={`${avgByRestaurant[r.restaurant_id].toFixed(2)} average (out of 5)`}
                      >
                        <span className="text-[9px] font-bold uppercase tracking-wide text-white/80">Rating</span>
                        <span className="font-display text-sm leading-none tracking-tight text-white drop-shadow-sm">
                          {starsExact(Math.round(avgByRestaurant[r.restaurant_id]))}
                        </span>
                      </div>
                    )}
                  </div>
                  <div className="mt-3 flex flex-wrap items-center gap-2">
                    <StatusPill variant="warning" className="!bg-white/30 !text-white !border-white/40">
                      {r.cuisine}
                    </StatusPill>
                    {mode === 'popular_orders' && orderCountById[r.restaurant_id] != null && (
                      <StatusPill variant="info" className="!bg-white/25 !text-white !border-white/35">
                        {orderCountById[r.restaurant_id]} orders
                      </StatusPill>
                    )}
                  </div>
                </div>
                <div className="p-4">
                  <p className="text-sm font-bold text-gobbl-teal">Tap to view menu →</p>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}

      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="text-sm font-semibold text-gobbl-ink/70">
          Showing {items.length} of {total}
        </p>
        <div className="flex gap-2">
          <Button variant="secondary" disabled={offset === 0 || loading} onClick={() => setOffset((o) => Math.max(0, o - PAGE))}>
            Previous
          </Button>
          <Button variant="secondary" disabled={offset + PAGE >= total || loading} onClick={() => setOffset((o) => o + PAGE)}>
            Next
          </Button>
        </div>
      </div>
    </div>
  )
}
