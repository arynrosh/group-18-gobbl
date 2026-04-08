import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
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
  const [picked, setPicked] = useState<RecommendedItem[] | null>(null)

  useEffect(() => {
    if (!user || !hasRole(user, ['customer'])) {
      setPicked(null)
      return
    }
    let cancelled = false
    ;(async () => {
      try {
        const data = await getRecommendations(user.username, 6)
        if (!cancelled) setPicked(data)
      } catch (e) {
        const msg = getApiErrorMessage(e, '')
        if (!cancelled) {
          setPicked([])
          if (msg && !msg.toLowerCase().includes('404')) toast.error(msg)
        }
      }
    })()
    return () => {
      cancelled = true
    }
  }, [user])

  return (
    <div className="space-y-10">
      <section className="mx-auto max-w-3xl">
        <p className="font-display text-sm font-bold uppercase tracking-widest text-gobbl-teal">Hungry? Same.</p>
        <h1 className="font-display mt-2 text-4xl font-extrabold leading-tight text-gobbl-ink md:text-5xl">
          Bold bites, silly name, <span className="text-gobbl-tomato">seriously good</span> delivery.
        </h1>
        <p className="mt-4 text-lg text-gobbl-ink/75">
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
      </section>

      {user && hasRole(user, ['customer']) && (
        <section>
          <div className="mb-4 flex items-end justify-between gap-4">
            <h2 className="font-display text-2xl font-bold text-gobbl-ink">Picked for you</h2>
            <Link to="/recommendations" className="text-sm font-bold text-gobbl-teal hover:underline">
              See all
            </Link>
          </div>
          {picked === null ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {Array.from({ length: 3 }).map((_, i) => (
                <Skeleton key={i} className="h-28 rounded-2xl" />
              ))}
            </div>
          ) : picked.length > 0 ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {picked.map((r) => (
                <Card key={`${r.menu_item_id}-${r.restaurant_id}`} hoverLift className="!p-4">
                  <p className="font-display text-lg font-bold leading-tight text-gobbl-ink">{r.food_item}</p>
                  <p className="mt-1 text-xs text-gobbl-ink/65">{r.restaurant_name}</p>
                  <p className="mt-1 text-[10px] font-bold uppercase tracking-wide text-gobbl-teal">{r.cuisine}</p>
                  <p className="mt-2 font-black text-gobbl-tomato">${r.order_value.toFixed(2)}</p>
                  <Link to={`/restaurants/${r.restaurant_id}`} className="mt-3 block">
                    <Button variant="mint" className="w-full !py-2 !text-xs">
                      View restaurant
                    </Button>
                  </Link>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <p className="text-gobbl-ink/75">
                Personalized picks show up once you have order history. Explore restaurants to get started.
              </p>
              <div className="mt-4 flex flex-wrap gap-2">
                <Link to="/restaurants">
                  <Button variant="secondary" className="!py-2 !text-sm">
                    Browse restaurants
                  </Button>
                </Link>
                <Link to="/recommendations">
                  <Button variant="mint" className="!py-2 !text-sm">
                    Open recommendations
                  </Button>
                </Link>
              </div>
            </Card>
          )}
        </section>
      )}
    </div>
  )
}
