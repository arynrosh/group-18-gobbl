import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { toast } from 'sonner'
import {
  browseRestaurants,
  searchRestaurantsByName,
  searchRestaurantsByCuisine,
} from '../features/restaurants/restaurantApi'
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
  const [mode, setMode] = useState<'browse' | 'name' | 'cuisine'>('browse')
  const [nameQ, setNameQ] = useState('')
  const [cuisineQ, setCuisineQ] = useState('')
  const debouncedName = useDebouncedValue(nameQ, 350)
  const debouncedCuisine = useDebouncedValue(cuisineQ, 350)

  const [items, setItems] = useState<Restaurant[]>([])
  const [total, setTotal] = useState(0)
  const [offset, setOffset] = useState(0)
  const [loading, setLoading] = useState(true)
  const [avgByRestaurant, setAvgByRestaurant] = useState<Record<number, number>>({})

  const load = useCallback(async () => {
    setLoading(true)
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
    if (!items.length) {
      setAvgByRestaurant({})
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
  }, [items])

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-display text-4xl font-extrabold text-gobbl-ink">Restaurants</h1>
        <p className="mt-1 text-gobbl-ink/70">Browse, search by name, or filter by cuisine — all backed by your API.</p>
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
          <p className="text-gobbl-ink/75">No restaurants match — try another search or browse all.</p>
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
                  <StatusPill variant="warning" className="mt-3 !bg-white/30 !text-white !border-white/40">
                    {r.cuisine}
                  </StatusPill>
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
