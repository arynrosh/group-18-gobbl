import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { toast } from 'sonner'
import { fetchMyOrders, fetchOrderStatus } from '../features/orders/orderApi'
import { useAuthStore, hasRole } from '../store/authStore'
import type { Order, OrderStatusRecord } from '../types'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { StatusPill } from '../components/ui/StatusPill'
import { Skeleton } from '../components/ui/Skeleton'

function itemCount(o: Order): number {
  return o.items.reduce((n, it) => n + (it.quantity || 0), 0)
}

export function MyOrdersPage() {
  const user = useAuthStore((s) => s.user)
  const [orders, setOrders] = useState<Order[] | null>(null)
  const [statusByOrderId, setStatusByOrderId] = useState<Record<string, OrderStatusRecord | null>>({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      setLoading(true)
      try {
        const list = await fetchMyOrders()
        if (cancelled) return
        setOrders(list)
        if (list.length > 0) {
          const entries = await Promise.all(
            list.map(async (o) => {
              try {
                const s = await fetchOrderStatus(o.order_id)
                return [o.order_id, s] as const
              } catch {
                return [o.order_id, null] as const
              }
            }),
          )
          if (!cancelled) setStatusByOrderId(Object.fromEntries(entries))
        } else {
          setStatusByOrderId({})
        }
      } catch (e) {
        if (!cancelled) {
          toast.error(getApiErrorMessage(e))
          setOrders([])
          setStatusByOrderId({})
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [])

  /** API returns orders in store order (oldest first); show newest on top. */
  const sortedOrders = useMemo(() => (orders == null ? null : [...orders].reverse()), [orders])

  if (!user || !hasRole(user, ['customer'])) {
    return (
      <Card>
        <p className="font-display text-lg font-bold text-gobbl-ink">Customers only</p>
        <p className="mt-2 text-gobbl-ink/75">Log in as a customer to see your orders.</p>
        <Link to="/login">
          <Button className="mt-4">Log in</Button>
        </Link>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display text-4xl font-extrabold text-gobbl-ink">My orders</h1>
        <p className="mt-1 text-sm text-gobbl-ink/65">
          When an order is <span className="font-semibold text-gobbl-ink">Complete</span>, use{' '}
          <span className="font-semibold text-gobbl-ink">Write review</span> to rate items from that order.
        </p>
        <p className="mt-0.5 text-xs text-gobbl-ink/50">GET /orders</p>
      </div>

      {loading ? (
        <Skeleton className="h-48" />
      ) : !sortedOrders?.length ? (
        <Card>
          <p className="text-gobbl-ink/75">No orders yet. Browse restaurants and place a cart to get started.</p>
          <Link to="/restaurants">
            <Button className="mt-4">Restaurants</Button>
          </Link>
        </Card>
      ) : (
        <div className="space-y-3">
          {sortedOrders.map((o) => {
            const st = statusByOrderId[o.order_id]
            return (
            <Card key={o.order_id} className="!border-gobbl-ink/10 !bg-white shadow-[0_1px_3px_rgba(45,42,50,0.08)]">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="font-mono text-sm font-bold text-gobbl-ink">{o.order_id}</p>
                  <p className="mt-1 text-sm text-gobbl-ink/65">
                    Restaurant #{o.restaurant_id} · {itemCount(o)} item(s)
                  </p>
                  {st ? (
                    <div className="mt-2 flex flex-wrap gap-2">
                      <StatusPill variant={st.complete ? 'success' : 'warning'}>
                        {st.complete ? 'Complete' : 'In progress'}
                      </StatusPill>
                    </div>
                  ) : null}
                </div>
                <div className="flex flex-wrap gap-2">
                  <Link to={`/orders/${encodeURIComponent(o.order_id)}`}>
                    <Button variant="secondary" className="!py-2 !text-sm">
                      Details
                    </Button>
                  </Link>
                  <Link to={`/orders/${encodeURIComponent(o.order_id)}/track`}>
                    <Button variant="mint" className="!py-2 !text-sm">
                      Track
                    </Button>
                  </Link>
                  {st?.complete ? (
                    <Link to={`/reviews/order/${encodeURIComponent(o.order_id)}`}>
                      <Button className="!py-2 !text-sm">Write review</Button>
                    </Link>
                  ) : null}
                </div>
              </div>
            </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}
