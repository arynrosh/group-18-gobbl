import { Link } from 'react-router-dom'
import { Card } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'

const tiles = [
  {
    to: '/admin/discounts',
    title: 'Discount codes',
    desc: 'Create promo codes, assign them to customers, and list every code (GET /discounts).',
    c: 'from-gobbl-tomato/90 to-gobbl-mango/80',
  },
  { to: '/admin/notifications', title: 'Notification studio', desc: 'Send manual + order lifecycle pings.', c: 'from-gobbl-teal/80 to-gobbl-mint/70' },
  { to: '/admin/analytics', title: 'Analytics playground', desc: 'Delivery times + popularity charts.', c: 'from-gobbl-lemon/90 to-gobbl-peach' },
]

export function AdminDashboardPage() {
  return (
    <div className="space-y-8">
      <h1 className="font-display text-4xl font-extrabold text-gobbl-ink">Admin mission control</h1>

      <Card className="border-2 border-gobbl-tomato/40 bg-gradient-to-r from-gobbl-peach/80 to-white/90">
        <p className="font-display text-sm font-bold uppercase tracking-widest text-gobbl-tomato">Discounts</p>
        <p className="mt-2 text-lg font-bold text-gobbl-ink">Manage promo codes</p>
        <p className="mt-1 max-w-2xl text-sm text-gobbl-ink/75">
          This is the admin screen for <code className="rounded bg-white/80 px-1">POST /discounts</code> and{' '}
          <code className="rounded bg-white/80 px-1">GET /discounts</code>. Use the sidebar <strong>Discount codes</strong> or the
          button below.
        </p>
        <Link to="/admin/discounts" className="mt-4 inline-block">
          <Button className="!px-8">Open discount codes</Button>
        </Link>
      </Card>

      <div className="grid gap-4 md:grid-cols-3">
        {tiles.map((t) => (
          <Card key={t.to} hoverLift className="!p-0 overflow-hidden">
            <div className={`bg-gradient-to-br ${t.c} p-5 text-white`}>
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
