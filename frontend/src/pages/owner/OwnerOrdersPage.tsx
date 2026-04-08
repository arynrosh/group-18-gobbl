import { useState } from 'react'
import { toast } from 'sonner'
import {
  fetchOrder,
  updateOrderStatus,
  completeOrder,
  fetchFulfillmentStatus,
  fulfillOrder,
} from '../../features/orders/orderApi'
import type { Order } from '../../types'
import { getApiErrorMessage } from '../../utils/apiError'
import { Card } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { Input, Label } from '../../components/ui/Input'
import { StatusPill } from '../../components/ui/StatusPill'
import { OrderLineItemsTable } from '../../components/OrderLineItemsTable'

const MSGS = ['placed', 'out for delivery', 'delayed', 'custom']

export function OwnerOrdersPage() {
  const [orderId, setOrderId] = useState('')
  const [customMsg, setCustomMsg] = useState('preparing')
  const [order, setOrder] = useState<Order | null>(null)
  const [ful, setFul] = useState<{ fulfillment_status?: string } | null>(null)
  const [busy, setBusy] = useState(false)

  async function load() {
    const id = orderId.trim()
    if (!id) return
    try {
      const o = await fetchOrder(id)
      setOrder(o)
      setOrderId(o.order_id)
      setFul(await fetchFulfillmentStatus(o.order_id))
    } catch (e) {
      toast.error(getApiErrorMessage(e))
      setOrder(null)
      setFul(null)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-extrabold text-gobbl-ink">Order operations</h1>
      <Card>
        <Label htmlFor="oid">order_id</Label>
        <div className="mt-2 flex flex-wrap gap-2">
          <Input id="oid" className="min-w-[240px] flex-1 font-mono" value={orderId} onChange={(e) => setOrderId(e.target.value)} />
          <Button type="button" variant="secondary" onClick={() => void load()}>
            Load order
          </Button>
        </div>
      </Card>

      {order && (
        <Card>
          <div className="flex flex-wrap gap-2">
            <StatusPill variant={order.sent ? 'success' : 'warning'}>{order.sent ? 'sent' : 'draft'}</StatusPill>
            {ful?.fulfillment_status && <StatusPill variant="info">{ful.fulfillment_status}</StatusPill>}
          </div>
          <p className="mt-3 font-mono text-sm">{order.order_id}</p>
          <div className="mt-4">
            <OrderLineItemsTable items={order.items} />
          </div>
          <div className="mt-6 flex flex-col gap-3">
            <p className="text-sm font-bold">PUT /orders/:id/status?msg=…</p>
            <div className="flex flex-wrap gap-2">
              {MSGS.filter((m) => m !== 'custom').map((m) => (
                <Button
                  key={m}
                  variant="secondary"
                  className="!py-2 !text-sm"
                  disabled={busy}
                  onClick={async () => {
                    setBusy(true)
                    try {
                      await updateOrderStatus(order.order_id, m)
                      toast.success('Status updated')
                      await load()
                    } catch (e) {
                      toast.error(getApiErrorMessage(e))
                    } finally {
                      setBusy(false)
                    }
                  }}
                >
                  {m}
                </Button>
              ))}
            </div>
            <div className="flex flex-wrap gap-2">
              <Input value={customMsg} onChange={(e) => setCustomMsg(e.target.value)} placeholder="custom msg" />
              <Button
                variant="mint"
                className="!py-2"
                disabled={busy}
                onClick={async () => {
                  setBusy(true)
                  try {
                    await updateOrderStatus(order.order_id, customMsg)
                    toast.success('Status updated')
                    await load()
                  } catch (e) {
                    toast.error(getApiErrorMessage(e))
                  } finally {
                    setBusy(false)
                  }
                }}
              >
                Send custom
              </Button>
            </div>
            <Button
              disabled={busy}
              onClick={async () => {
                setBusy(true)
                try {
                  await completeOrder(order.order_id)
                  toast.success('Order marked complete and closed')
                  setOrder(null)
                  setFul(null)
                  setOrderId('')
                } catch (e) {
                  toast.error(getApiErrorMessage(e))
                } finally {
                  setBusy(false)
                }
              }}
            >
              Complete order (PUT /orders/:id/complete)
            </Button>
            <Button
              variant="secondary"
              disabled={busy}
              onClick={async () => {
                setBusy(true)
                try {
                  await fulfillOrder(order.order_id)
                  toast.success('Fulfillment requested')
                  await load()
                } catch (e) {
                  toast.error(getApiErrorMessage(e))
                } finally {
                  setBusy(false)
                }
              }}
            >
              Fulfill (POST /orders/:id/fulfill — needs payment)
            </Button>
          </div>
        </Card>
      )}
    </div>
  )
}
