import { useCallback, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { toast } from 'sonner'
import { fetchOrderStatus, fetchFulfillmentStatus } from '../features/orders/orderApi'
import type { OrderStatusRecord } from '../types'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { StatusPill } from '../components/ui/StatusPill'

export function OrderTrackPage() {
  const { orderId } = useParams()
  const [status, setStatus] = useState<OrderStatusRecord | null>(null)
  const [ful, setFul] = useState<{ fulfillment_status?: string } | null>(null)
  const [polling, setPolling] = useState(false)

  const load = useCallback(async () => {
    if (!orderId) return
    try {
      const [s, f] = await Promise.all([fetchOrderStatus(orderId), fetchFulfillmentStatus(orderId)])
      setStatus(s)
      setFul(f)
    } catch (e) {
      toast.error(getApiErrorMessage(e))
    }
  }, [orderId])

  useEffect(() => {
    if (!orderId) return
    let cancelled = false
    ;(async () => {
      try {
        const [s, f] = await Promise.all([fetchOrderStatus(orderId), fetchFulfillmentStatus(orderId)])
        if (!cancelled) {
          setStatus(s)
          setFul(f)
        }
      } catch (e) {
        if (!cancelled) toast.error(getApiErrorMessage(e))
      }
    })()
    return () => {
      cancelled = true
    }
  }, [orderId])

  useEffect(() => {
    if (!polling || !orderId) return
    const id = window.setInterval(() => void load(), 5000)
    return () => window.clearInterval(id)
  }, [polling, orderId, load])

  if (!orderId) return null

  return (
    <div className="mx-auto max-w-xl space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="font-display text-3xl font-extrabold text-gobbl-ink">Order tracker</h1>
        <div className="flex gap-2">
          <Button variant="secondary" className="!py-2 !text-sm" onClick={() => void load()}>
            Refresh
          </Button>
          <Button variant={polling ? 'primary' : 'secondary'} className="!py-2 !text-sm" onClick={() => setPolling((p) => !p)}>
            {polling ? 'Stop polling' : 'Poll every 5s'}
          </Button>
        </div>
      </div>
      <Card>
        <p className="font-mono text-xs text-gobbl-ink/60">{orderId}</p>
        {status ? (
          <div className="mt-4 space-y-4">
            <div className="flex flex-wrap items-center gap-2">
              <StatusPill variant="info">Status: {status.current}</StatusPill>
              <StatusPill variant={status.complete ? 'success' : 'warning'}>
                {status.complete ? 'complete' : 'in progress'}
              </StatusPill>
            </div>
            <ol className="space-y-3 border-l-4 border-gobbl-mango pl-4">
              {['pending', 'placed', 'out for delivery', 'delayed', 'delivered'].map((step) => {
                const active = status.current === step || (step === 'delivered' && status.complete)
                return (
                <li
                  key={step}
                  className={
                    active ? 'font-black text-gobbl-tomato' : 'text-gobbl-ink/55 line-through decoration-wavy'
                  }
                >
                  {step}
                </li>
              )})}
            </ol>
            <p className="text-xs text-gobbl-ink/55">
              Timeline labels are a friendly UI hint — your backend uses free-text status updates.
            </p>
          </div>
        ) : (
          <p className="mt-4 text-gobbl-ink/70">Loading…</p>
        )}
        {ful && (
          <p className="mt-4 text-sm font-bold">
            Fulfillment: <span className="text-gobbl-teal">{ful.fulfillment_status ?? 'pending'}</span>
          </p>
        )}
      </Card>
      <Link to="/cart">
        <Button variant="ghost">Back to cart</Button>
      </Link>
    </div>
  )
}
