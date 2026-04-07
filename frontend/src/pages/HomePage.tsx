import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { toast } from 'sonner'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { useAuthStore, hasRole } from '../store/authStore'
import { getRecommendations } from '../features/recommendations/recommendationApi'
import type { RecommendedItem } from '../types'
import { getApiErrorMessage } from '../utils/apiError'
import { Skeleton } from '../components/ui/Skeleton'

export function HomePage() {
  const user = useAuthStore((s) => s.user)
  const [recs, setRecs] = useState<RecommendedItem[] | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!user || !hasRole(user, ['customer'])) {
      setRecs(null)
      return
    }
    let cancelled = false
    ;(async () => {
      setLoading(true)
      try {
        const data = await getRecommendations(user.username, 6)
        if (!cancelled) setRecs(data)
      } catch (e) {
        if (!cancelled) setRecs([])
        const msg = getApiErrorMessage(e, '')
        if (msg && !msg.includes('404')) toast.message(msg)
      } finally {
        if (!cancelled) setLoading(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [user])

  return (
    <div className="space-y-10">
      <section className="grid items-center gap-8 lg:grid-cols-2">
        <div>
          <p className="font-display text-sm font-bold uppercase tracking-widest text-gobbl-teal">Hungry? Same.</p>
          <h1 className="font-display mt-2 text-4xl font-extrabold leading-tight text-gobbl-ink md:text-5xl">
            Bold bites, silly name, <span className="text-gobbl-tomato">seriously good</span> delivery.
          </h1>
          <p className="mt-4 max-w-xl text-lg text-gobbl-ink/75">
            Gobbl connects to your FastAPI backend for real orders, promos, drivers, and reviews — wrapped in a playful,
            DoorDash-inspired UI.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link to="/restaurants">
              <Button>Find food</Button>
            </Link>
            {!user && (
              <Link to="/register">
                <Button variant="secondary">Create an account</Button>
              </Link>
            )}
          </div>
        </div>
        <Card hoverLift className="relative overflow-hidden !p-0">
          <div className="bg-gradient-to-br from-gobbl-mango via-gobbl-lemon to-gobbl-mint p-8 text-gobbl-ink">
            <p className="font-display text-2xl font-bold">Today&apos;s vibe</p>
            <p className="mt-2 text-lg font-semibold opacity-90">Crispy edges. Soft centers. Zero boring beige.</p>
            <div className="mt-6 grid grid-cols-2 gap-3 text-sm font-bold">
              <div className="rounded-2xl bg-white/40 px-3 py-2">Warm reds & oranges</div>
              <div className="rounded-2xl bg-white/40 px-3 py-2">Teal accents</div>
              <div className="rounded-2xl bg-white/40 px-3 py-2">Rounded cards</div>
              <div className="rounded-2xl bg-white/40 px-3 py-2">Big happy buttons</div>
            </div>
          </div>
        </Card>
      </section>

      {user && hasRole(user, ['customer']) && (
        <section>
          <div className="mb-4 flex items-end justify-between gap-4">
            <h2 className="font-display text-2xl font-bold text-gobbl-ink">Picked for you</h2>
            <Link to="/recommendations" className="text-sm font-bold text-gobbl-teal hover:underline">
              See all
            </Link>
          </div>
          {loading && (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              <Skeleton className="h-28" />
              <Skeleton className="h-28" />
              <Skeleton className="h-28" />
            </div>
          )}
          {!loading && recs && recs.length === 0 && (
            <Card>
              <p className="text-gobbl-ink/75">
                No recommendations yet — order something tasty first! The backend returns 404 until you have history.
              </p>
            </Card>
          )}
          {!loading && recs && recs.length > 0 && (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {recs.map((r) => (
                <Card key={`${r.menu_item_id}-${r.restaurant_id}`} hoverLift>
                  <p className="font-display text-lg font-bold text-gobbl-ink">{r.food_item}</p>
                  <p className="text-sm text-gobbl-ink/70">{r.restaurant_name}</p>
                  <p className="mt-2 text-xs font-bold uppercase text-gobbl-teal">{r.cuisine}</p>
                  <p className="mt-3 text-lg font-extrabold text-gobbl-tomato">${r.order_value.toFixed(2)}</p>
                  <Link to={`/restaurants/${r.restaurant_id}`}>
                    <Button className="mt-4 w-full !py-2 !text-sm" variant="mint">
                      View restaurant
                    </Button>
                  </Link>
                </Card>
              ))}
            </div>
          )}
        </section>
      )}
    </div>
  )
}
