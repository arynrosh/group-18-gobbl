import { Link } from 'react-router-dom'
import { Card } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'

const tiles = [
  { to: '/owner/menu', title: 'Menu studio', desc: 'CRUD items for a restaurant_id you manage.', color: 'from-gobbl-mango/80 to-gobbl-tomato/80' },
  { to: '/owner/delivery', title: 'Delivery ops', desc: 'Drivers, auto-assign, manual assign.', color: 'from-gobbl-teal/70 to-gobbl-mint/70' },
  { to: '/owner/notifications', title: 'Restaurant pings', desc: 'GET /notifications/restaurant/{id}', color: 'from-gobbl-lemon/80 to-gobbl-mango/70' },
  { to: '/owner/orders', title: 'Order flow', desc: 'Update status, complete, fulfillment peek.', color: 'from-gobbl-peach to-gobbl-mango/60' },
]

export function OwnerDashboardPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-display text-4xl font-extrabold text-gobbl-ink">Owner hub</h1>
        <p className="mt-2 text-gobbl-ink/70">
          The backend does not link users to restaurants — pick a <span className="font-bold">restaurant_id</span> on the menu
          page (stored locally) before editing.
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {tiles.map((t) => (
          <Card key={t.to} hoverLift className="!p-0 overflow-hidden">
            <div className={`bg-gradient-to-br ${t.color} p-5 text-white`}>
              <h2 className="font-display text-2xl font-bold">{t.title}</h2>
              <p className="mt-2 text-sm font-semibold text-white/90">{t.desc}</p>
            </div>
            <div className="p-4">
              <Link to={t.to}>
                <Button className="w-full !py-2">Open</Button>
              </Link>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
