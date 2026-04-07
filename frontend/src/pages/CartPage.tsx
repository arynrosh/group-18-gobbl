import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { toast } from 'sonner'
import { useCartStore } from '../store/cartStore'
import { useAuthStore, hasRole } from '../store/authStore'
import { fetchOrder, removeOrderItem } from '../features/orders/orderApi'
import type { Order } from '../types'
import { computeCostBreakdown, COST_DELIVERY_FEE, COST_TAX_RATE } from '../utils/costBreakdown'
import { getApiErrorMessage } from '../utils/apiError'
import { normalizeOrderDietRestrictions } from '../utils/dietRestrictions'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input, Label } from '../components/ui/Input'
import { StatusPill } from '../components/ui/StatusPill'
import { Skeleton } from '../components/ui/Skeleton'
import { OrderLineItemsTable } from '../components/OrderLineItemsTable'

export function CartPage() {
  const navigate = useNavigate()
  const user = useAuthStore((s) => s.user)
  const { orderId, deliveryDistance, deliveryTime, patchDelivery, clear } = useCartStore()
  const [order, setOrder] = useState<Order | null>(null)
  const [loading, setLoading] = useState(false)
  const [busy, setBusy] = useState(false)

  async function refresh() {
    if (!orderId) {
      setOrder(null)
      return
    }
    setLoading(true)
    try {
      const o = await fetchOrder(orderId)
      setOrder(o)
    } catch (e) {
      toast.error(getApiErrorMessage(e))
      setOrder(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void refresh()
    // eslint-disable-next-line react-hooks/exhaustive-deps -- refresh when orderId changes
  }, [orderId])

  const cost = useMemo(() => (order ? computeCostBreakdown(order) : null), [order])

  if (!user || !hasRole(user, ['customer'])) {
    return (
      <Card>
        <p className="font-display text-lg font-bold text-gobbl-ink">Customers only</p>
        <p className="mt-2 text-gobbl-ink/75">Log in as a customer to view your cart.</p>
        <Link to="/login">
          <Button className="mt-4">Log in</Button>
        </Link>
      </Card>
    )
  }

  if (!orderId) {
    return (
      <Card>
        <h1 className="font-display text-3xl font-extrabold text-gobbl-ink">Your cart is empty</h1>
        <p className="mt-2 text-gobbl-ink/75">Pick a restaurant and add items to start an order.</p>
        <Link to="/restaurants">
          <Button className="mt-6">Browse restaurants</Button>
        </Link>
      </Card>
    )
  }

  const sent = order?.sent
  const dr = normalizeOrderDietRestrictions(order)

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="font-display text-4xl font-extrabold text-gobbl-ink">Cart</h1>
          <p className="text-sm text-gobbl-ink/65">
            Order <span className="font-mono font-bold">{orderId}</span>
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          {sent ? <StatusPill variant="success">Sent</StatusPill> : <StatusPill variant="warning">Draft</StatusPill>}
          <Button variant="secondary" disabled={busy} onClick={() => void refresh()}>
            Refresh
          </Button>
          <Button
            variant="ghost"
            disabled={busy || sent}
            onClick={() => {
              clear()
              toast.message('Cart cleared locally ? backend order may still exist.')
            }}
          >
            Forget cart
          </Button>
        </div>
      </div>

      <Card>
        <div className="flex items-center justify-between gap-3">
          <h2 className="font-display text-lg font-bold text-gobbl-ink">Diet restrictions on this order</h2>
          <Link to="/diet-restrictions">
            <Button variant="secondary" className="!py-2 !text-sm">
              Manage diet
            </Button>
          </Link>
        </div>
        {dr ? (
          <div className="mt-3 flex flex-wrap gap-2">
            {dr.diet_restrictions.length ? (
              dr.diet_restrictions.map((r) => (
                <StatusPill key={r} variant="info">
                  {r}
                </StatusPill>
              ))
            ) : (
              <p className="text-sm text-gobbl-ink/70">No restrictions currently saved for this user.</p>
            )}
          </div>
        ) : (
          <p className="mt-3 text-sm text-gobbl-ink/70">
            This order has no diet restriction metadata yet. If you just updated restrictions, create a new order to apply them.
          </p>
        )}
      </Card>

      <Card>
        <h2 className="font-display text-lg font-bold text-gobbl-ink">Delivery hints</h2>
        <p className="text-xs text-gobbl-ink/60">
          These were sent as query params when the order was created. To change them, start a new order (backend shape).
        </p>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <div>
            <Label htmlFor="dd">delivery_distance</Label>
            <Input
              id="dd"
              type="number"
              disabled={sent}
              value={deliveryDistance}
              onChange={(e) => patchDelivery({ deliveryDistance: Number(e.target.value) })}
            />
          </div>
          <div>
            <Label htmlFor="dt">delivery_time (minutes)</Label>
            <Input
              id="dt"
              type="number"
              disabled={sent}
              value={deliveryTime ?? ''}
              onChange={(e) => patchDelivery({ deliveryTime: e.target.value === '' ? null : Number(e.target.value) })}
            />
          </div>
        </div>
      </Card>

      {loading && !order ? (
        <Skeleton className="h-48" />
      ) : order ? (
        <Card>
          <h2 className="font-display text-lg font-bold text-gobbl-ink">Items</h2>
          <p className="mt-1 text-xs text-gobbl-ink/55">
            Unit price is per item; line total is quantity ? unit price.
          </p>
          <div className="mt-4">
            {order.items.length === 0 ? (
              <p className="text-sm text-gobbl-ink/70">No line items yet.</p>
            ) : (
              <OrderLineItemsTable
                items={order.items}
                renderAction={(it) => (
                  <Button
                    variant="secondary"
                    className="!py-1.5 !text-xs"
                    disabled={sent || busy}
                    onClick={async () => {
                      setBusy(true)
                      try {
                        await removeOrderItem(orderId, it.food_item)
                        toast.success('Removed')
                        await refresh()
                      } catch (e) {
                        toast.error(getApiErrorMessage(e))
                      } finally {
                        setBusy(false)
                      }
                    }}
                  >
                    Remove
                  </Button>
                )}
              />
            )}
          </div>
        </Card>
      ) : null}

      <Card className="!border-gobbl-ink/10 !bg-white shadow-[0_1px_3px_rgba(45,42,50,0.08)]">
        <div>
          <h2 className="font-display text-lg font-bold text-gobbl-ink">Cost breakdown</h2>
          <p className="mt-1 text-xs text-gobbl-ink/50">
            {(COST_TAX_RATE * 100).toFixed(0)}% tax � ${COST_DELIVERY_FEE.toFixed(2)} delivery (same as server rules)
          </p>
        </div>
        {cost ? (
          <dl className="mt-4 overflow-hidden rounded-2xl border border-gobbl-ink/10 bg-white text-sm">
            <div className="flex items-center justify-between gap-4 border-b border-gobbl-ink/8 px-4 py-3">
              <dt className="text-gobbl-ink/65">Subtotal</dt>
              <dd className="tabular-nums font-semibold text-gobbl-ink">${cost.subtotal.toFixed(2)}</dd>
            </div>
            <div className="flex items-center justify-between gap-4 border-b border-gobbl-ink/8 px-4 py-3">
              <dt className="text-gobbl-ink/65">Tax</dt>
              <dd className="tabular-nums font-semibold text-gobbl-ink">${cost.tax.toFixed(2)}</dd>
            </div>
            <div className="flex items-center justify-between gap-4 border-b border-gobbl-ink/8 px-4 py-3">
              <dt className="text-gobbl-ink/65">Delivery</dt>
              <dd className="tabular-nums font-semibold text-gobbl-ink">${cost.delivery_fee.toFixed(2)}</dd>
            </div>
            <div className="flex items-center justify-between gap-4 bg-gobbl-ink/[0.02] px-4 py-3.5">
              <dt className="font-display text-base font-bold text-gobbl-ink">Total</dt>
              <dd className="tabular-nums font-display text-xl font-extrabold text-gobbl-ink">${cost.total.toFixed(2)}</dd>
            </div>
          </dl>
        ) : (
          <p className="mt-3 text-sm text-gobbl-ink/55">
            {loading ? 'Loading order?' : 'Load your order to see totals.'}
          </p>
        )}
      </Card>

      <div className="space-y-2">
        <div className="flex flex-wrap gap-3">
        <Button
          disabled={!order || busy || !order.items.length}
          onClick={() => navigate(`/checkout?orderId=${encodeURIComponent(orderId)}`)}
        >
          Go to checkout
        </Button>
        <Link to={`/orders/${orderId}/track`}>
          <Button variant="mint" disabled={!order}>
            Track
          </Button>
        </Link>
        </div>
        <p className="text-xs text-gobbl-ink/55">
          You pay at checkout first; the restaurant is notified right after your payment clears.
        </p>
      </div>
    </div>
  )
}
