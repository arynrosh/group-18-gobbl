import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { toast } from 'sonner'
import { fetchOrder, calculateCost, fetchFulfillmentStatus } from '../features/orders/orderApi'
import { getPaymentByOrder } from '../features/payments/paymentApi'
import type { CostBreakdown, Order, PaymentRecord } from '../types'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { StatusPill } from '../components/ui/StatusPill'
import { Skeleton } from '../components/ui/Skeleton'

export function OrderDetailPage() {
  const { orderId } = useParams()
  const [order, setOrder] = useState<Order | null>(null)
  const [cost, setCost] = useState<CostBreakdown | null>(null)
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
          setCost(await calculateCost(orderId))
        } catch {
          setCost(null)
        }
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

  if (!orderId) return null
  if (!order) return <Skeleton className="h-48" />

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
        <ul className="mt-4 space-y-2 text-sm">
          {order.items.map((i) => (
            <li key={`${i.menu_item_id}-${i.food_item}`} className="flex justify-between gap-4">
              <span>
                {i.food_item} × {i.quantity}
              </span>
              <span className="font-bold">${(i.order_value * i.quantity).toFixed(2)}</span>
            </li>
          ))}
        </ul>
      </Card>
      {cost && (
        <Card>
          <p className="text-lg font-bold">
            Total (estimate){' '}
            <span className="text-gobbl-tomato">${cost.total.toFixed(2)}</span>
          </p>
        </Card>
      )}
    </div>
  )
}
