import { useState } from 'react'
import { toast } from 'sonner'
import {
  sendNotification,
  orderPlaced,
  orderOutForDelivery,
  orderDelivered,
  orderDelayed,
} from '../../features/notifications/notificationApi'
import { getApiErrorMessage } from '../../utils/apiError'
import { Card } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { Input, Label } from '../../components/ui/Input'

export function AdminNotificationsPage() {
  const [busy, setBusy] = useState(false)

  const [customer_id, setCustomerId] = useState('')
  const [order_id, setOrderId] = useState('')
  const [restaurant_id, setRestaurantId] = useState('1')
  const [message, setMessage] = useState('Hello from Gobbl admin!')
  const [driver_name, setDriverName] = useState('Casey')
  const [delay_minutes, setDelayMinutes] = useState('12')

  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-extrabold text-gobbl-ink">Notifications</h1>

      <Card>
        <h2 className="font-display text-lg font-bold">Custom send</h2>
        <p className="text-xs text-gobbl-ink/55">POST /notifications/send</p>
        <form
          className="mt-4 grid gap-4 md:grid-cols-2"
          onSubmit={async (e) => {
            e.preventDefault()
            setBusy(true)
            try {
              await sendNotification({
                customer_id,
                order_id: order_id || null,
                restaurant_id: Number(restaurant_id),
                message,
              })
              toast.success('Sent')
            } catch (err) {
              toast.error(getApiErrorMessage(err))
            } finally {
              setBusy(false)
            }
          }}
        >
          <div>
            <Label htmlFor="cid">customer_id</Label>
            <Input id="cid" value={customer_id} onChange={(e) => setCustomerId(e.target.value)} required />
          </div>
          <div>
            <Label htmlFor="oid">order_id (optional)</Label>
            <Input id="oid" value={order_id} onChange={(e) => setOrderId(e.target.value)} />
          </div>
          <div>
            <Label htmlFor="rid">restaurant_id</Label>
            <Input id="rid" type="number" value={restaurant_id} onChange={(e) => setRestaurantId(e.target.value)} required />
          </div>
          <div className="md:col-span-2">
            <Label htmlFor="msg">message</Label>
            <Input id="msg" value={message} onChange={(e) => setMessage(e.target.value)} required />
          </div>
          <Button type="submit" disabled={busy}>
            Send
          </Button>
        </form>
      </Card>

      <Card>
        <h2 className="font-display text-lg font-bold">Order event shortcuts</h2>
        <p className="text-xs text-gobbl-ink/55">POST /order-notifications/* (admin only)</p>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          <div>
            <Label>order_id</Label>
            <Input className="mt-1 font-mono text-xs" value={order_id} onChange={(e) => setOrderId(e.target.value)} />
          </div>
          <div>
            <Label>customer_id</Label>
            <Input className="mt-1" value={customer_id} onChange={(e) => setCustomerId(e.target.value)} />
          </div>
          <div>
            <Label>restaurant_id</Label>
            <Input className="mt-1" type="number" value={restaurant_id} onChange={(e) => setRestaurantId(e.target.value)} />
          </div>
        </div>
        <div className="mt-4 flex flex-wrap gap-2">
          <Button
            variant="secondary"
            className="!py-2 !text-sm"
            disabled={busy}
            onClick={async () => {
              setBusy(true)
              try {
                await orderPlaced({ order_id, customer_id, restaurant_id: Number(restaurant_id) })
                toast.success('Placed notification')
              } catch (e) {
                toast.error(getApiErrorMessage(e))
              } finally {
                setBusy(false)
              }
            }}
          >
            Placed
          </Button>
          <Button
            variant="secondary"
            className="!py-2 !text-sm"
            disabled={busy}
            onClick={async () => {
              setBusy(true)
              try {
                await orderOutForDelivery({
                  order_id,
                  customer_id,
                  restaurant_id: Number(restaurant_id),
                  driver_name,
                })
                toast.success('Out for delivery')
              } catch (e) {
                toast.error(getApiErrorMessage(e))
              } finally {
                setBusy(false)
              }
            }}
          >
            Out for delivery
          </Button>
          <Button
            variant="secondary"
            className="!py-2 !text-sm"
            disabled={busy}
            onClick={async () => {
              setBusy(true)
              try {
                await orderDelivered({ order_id, customer_id, restaurant_id: Number(restaurant_id) })
                toast.success('Delivered')
              } catch (e) {
                toast.error(getApiErrorMessage(e))
              } finally {
                setBusy(false)
              }
            }}
          >
            Delivered
          </Button>
          <div className="flex flex-wrap items-center gap-2">
            <Input className="max-w-[120px]" value={delay_minutes} onChange={(e) => setDelayMinutes(e.target.value)} />
            <Button
              variant="secondary"
              className="!py-2 !text-sm"
              disabled={busy}
              onClick={async () => {
                setBusy(true)
                try {
                  await orderDelayed({
                    order_id,
                    customer_id,
                    restaurant_id: Number(restaurant_id),
                    delay_minutes: Number(delay_minutes),
                  })
                  toast.success('Delayed')
                } catch (e) {
                  toast.error(getApiErrorMessage(e))
                } finally {
                  setBusy(false)
                }
              }}
            >
              Delayed
            </Button>
          </div>
        </div>
        <div className="mt-3">
          <Label>driver_name (out for delivery)</Label>
          <Input className="mt-1" value={driver_name} onChange={(e) => setDriverName(e.target.value)} />
        </div>
      </Card>
    </div>
  )
}
