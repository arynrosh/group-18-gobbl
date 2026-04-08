import { Link } from 'react-router-dom'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { useAuthStore, hasRole } from '../store/authStore'

export function HomePage() {
  const user = useAuthStore((s) => s.user)

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
        </section>
      )}
    </div>
  )
}
