import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { toast } from 'sonner'
import { useCartStore } from '../store/cartStore'
import { useAuthStore, hasRole } from '../store/authStore'
import {
  fetchOrder,
  removeOrderItem,
  sendOrder,
  calculateCost,
  addMysteryBag,
} from '../features/orders/orderApi'
import type { CostBreakdown, Order } from '../types'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input, Label } from '../components/ui/Input'
import { StatusPill } from '../components/ui/StatusPill'
import { Skeleton } from '../components/ui/Skeleton'

export function CartPage() {
  const navigate = useNavigate()
  const user = useAuthStore((s) => s.user)
  const { orderId, deliveryDistance, deliveryTime, patchDelivery, clear } = useCartStore()
  const [order, setOrder] = useState<Order | null>(null)
  const [cost, setCost] = useState<CostBreakdown | null>(null)
  const [loading, setLoading] = useState(false)
  const [budget, setBudget] = useState('25')
  const [mysteryOpen, setMysteryOpen] = useState(false)
  const [busy, setBusy] = useState(false)

  async function refresh() {
    if (!orderId) {
      setOrder(null)
      setCost(null)
      return
    }
    setLoading(true)
    try {
      const o = await fetchOrder(orderId)
      setOrder(o)
      try {
        const c = await calculateCost(orderId)
        setCost(c)
      } catch {
        setCost(null)
      }
    } catch (e) {
      toast.error(getApiErrorMessage(e))
      setOrder(null)
      setCost(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void refresh()
    // eslint-disable-next-line react-hooks/exhaustive-deps -- refresh when orderId changes
  }, [orderId])

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
              toast.message('Cart cleared locally — backend order may still exist.')
            }}
          >
            Forget cart
          </Button>
        </div>
      </div>

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
          <ul className="mt-4 space-y-3">
            {order.items.length === 0 && <li className="text-gobbl-ink/70">No line items yet.</li>}
            {order.items.map((it) => (
              <li
                key={`${it.menu_item_id}-${it.food_item}`}
                className="flex flex-wrap items-center justify-between gap-3 rounded-2xl bg-white/70 px-4 py-3"
              >
                <div>
                  <p className="font-bold text-gobbl-ink">{it.food_item}</p>
                  <p className="text-xs text-gobbl-ink/60">
                    qty {it.quantity} × ${it.order_value.toFixed(2)}
                  </p>
                </div>
                <Button
                  variant="secondary"
                  className="!py-2 !text-sm"
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
              </li>
            ))}
          </ul>
        </Card>
      ) : null}

      <Card>
        <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="font-display text-lg font-bold text-gobbl-ink">Cost breakdown</h2>
            <p className="text-xs text-gobbl-ink/60">POST /cost/calculate/:order_id</p>
          </div>
          <Button variant="mint" disabled={loading || !orderId} onClick={() => void refresh()}>
            Recalculate
          </Button>
        </div>
        {cost ? (
          <dl className="mt-4 grid grid-cols-2 gap-3 text-sm md:grid-cols-4">
            <div className="rounded-2xl bg-gobbl-peach/40 px-3 py-2">
              <dt className="text-xs font-bold uppercase text-gobbl-ink/60">Subtotal</dt>
              <dd className="text-lg font-black">${cost.subtotal.toFixed(2)}</dd>
            </div>
            <div className="rounded-2xl bg-gobbl-lemon/35 px-3 py-2">
              <dt className="text-xs font-bold uppercase text-gobbl-ink/60">Tax</dt>
              <dd className="text-lg font-black">${cost.tax.toFixed(2)}</dd>
            </div>
            <div className="rounded-2xl bg-gobbl-teal/15 px-3 py-2">
              <dt className="text-xs font-bold uppercase text-gobbl-ink/60">Delivery</dt>
              <dd className="text-lg font-black">${cost.delivery_fee.toFixed(2)}</dd>
            </div>
            <div className="rounded-2xl bg-gobbl-mint/25 px-3 py-2">
              <dt className="text-xs font-bold uppercase text-gobbl-ink/60">Total</dt>
              <dd className="text-lg font-black text-gobbl-tomato">${cost.total.toFixed(2)}</dd>
            </div>
          </dl>
        ) : (
          <p className="mt-3 text-sm text-gobbl-ink/65">
            Cost unavailable (empty cart or backend validation). Note: backend loads orders with strict schemas — if calculation
            fails, check server logs.
          </p>
        )}
      </Card>

      <Card className="border-2 border-dashed border-gobbl-mango/70 bg-gradient-to-br from-gobbl-lemon/25 to-gobbl-mango/20">
        <button
          type="button"
          className="flex w-full items-center justify-between gap-3 text-left"
          onClick={() => setMysteryOpen((v) => !v)}
        >
          <div>
            <h2 className="font-display text-xl font-extrabold text-gobbl-ink">Mystery bag ✨</h2>
            <p className="text-sm text-gobbl-ink/70">POST /orders/:id/mystery-bag — backend extends items silently; we re-fetch.</p>
          </div>
          <span className="font-display text-2xl">{mysteryOpen ? '−' : '+'}</span>
        </button>
        {mysteryOpen && (
          <div className="mt-4 flex flex-col gap-3 md:flex-row md:items-end">
            <div className="min-w-[200px] flex-1">
              <Label htmlFor="bud">Budget</Label>
              <Input id="bud" type="number" step="0.01" min="0.01" value={budget} onChange={(e) => setBudget(e.target.value)} />
            </div>
            <Button
              disabled={sent || busy}
              onClick={async () => {
                setBusy(true)
                try {
                  const b = Number(budget)
                  await addMysteryBag(orderId, b)
                  toast.success('Mystery bag added — revealing…')
                  await refresh()
                } catch (e) {
                  toast.error(getApiErrorMessage(e))
                } finally {
                  setBusy(false)
                }
              }}
            >
              Surprise me
            </Button>
          </div>
        )}
      </Card>

      <div className="flex flex-wrap gap-3">
        <Button
          variant="secondary"
          disabled={!order || sent || busy || !order.items.length}
          onClick={async () => {
            setBusy(true)
            try {
              await sendOrder(orderId)
              toast.success('Order sent!')
              await refresh()
            } catch (e) {
              toast.error(getApiErrorMessage(e))
            } finally {
              setBusy(false)
            }
          }}
        >
          Send order
        </Button>
        <Button
          disabled={!order || !order.sent || busy}
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
    </div>
  )
}
