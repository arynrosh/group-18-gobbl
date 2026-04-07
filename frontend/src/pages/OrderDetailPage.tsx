import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { toast } from 'sonner'
import { fetchOrder, fetchFulfillmentStatus } from '../features/orders/orderApi'
import { getPaymentByOrder } from '../features/payments/paymentApi'
import type { Order, PaymentRecord } from '../types'
import { computeCostBreakdown } from '../utils/costBreakdown'
import { getApiErrorMessage } from '../utils/apiError'
import { normalizeOrderDietRestrictions } from '../utils/dietRestrictions'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { StatusPill } from '../components/ui/StatusPill'
import { Skeleton } from '../components/ui/Skeleton'
import { OrderLineItemsTable } from '../components/OrderLineItemsTable'

export function OrderDetailPage() {
  const { orderId } = useParams()
  const [order, setOrder] = useState<Order | null>(null)
  const [pay, setPay] = useState<PaymentRecord | null | undefined>(undefined)
  const [ful, setFul] = useState<{ order_id: string; fulfillment_status?: string } | null>(null)

  useEffect(() => {
    if (!orderId) return
    let cancelled = false
    ;(async () => {
      try {
        const o = await fetchOrder(orderId)
        if (cancelled) return
        setOrder(o)
        try {
          setPay(await getPaymentByOrder(orderId))
        } catch {
          setPay(null)
        }
        try {
          setFul(await fetchFulfillmentStatus(orderId))
        } catch {
          setFul(null)
        }
      } catch (e) {
        if (!cancelled) toast.error(getApiErrorMessage(e))
      }
    })()
    return () => {
      cancelled = true
    }
  }, [orderId])

  const cost = useMemo(() => (order ? computeCostBreakdown(order) : null), [order])

  if (!orderId) return null
  if (!order) return <Skeleton className="h-48" />

  const dr = normalizeOrderDietRestrictions(order)

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="font-display text-3xl font-extrabold text-gobbl-ink">Order</h1>
        <Link to={`/orders/${orderId}/track`}>
          <Button variant="mint">Track</Button>
        </Link>
      </div>
      <Card>
        <div className="flex flex-wrap gap-2">
          <StatusPill variant={order.sent ? 'success' : 'warning'}>{order.sent ? 'sent' : 'draft'}</StatusPill>
          {pay && <StatusPill variant="info">paid</StatusPill>}
          {ful?.fulfillment_status && <StatusPill variant="success">{ful.fulfillment_status}</StatusPill>}
        </div>
        <p className="mt-3 font-mono text-sm">{order.order_id}</p>
        {!!dr?.diet_restrictions?.length && (
          <div className="mt-3 flex flex-wrap gap-2">
            {dr.diet_restrictions.map((r) => (
              <StatusPill key={r} variant="info">
                {r}
              </StatusPill>
            ))}
          </div>
        )}
        <div className="mt-4">
          <h2 className="font-display text-lg font-bold text-gobbl-ink">Line items</h2>
          <p className="mt-1 text-xs text-gobbl-ink/55">Quantity, unit price, and line total.</p>
          <div className="mt-3">
            <OrderLineItemsTable items={order.items} />
          </div>
        </div>
      </Card>
      {cost && (
        <Card className="!border-gobbl-ink/10 !bg-white shadow-[0_1px_3px_rgba(45,42,50,0.08)]">
          <h2 className="font-display text-lg font-bold text-gobbl-ink">Cost (estimate)</h2>
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
        </Card>
      )}
    </div>
  )
}
