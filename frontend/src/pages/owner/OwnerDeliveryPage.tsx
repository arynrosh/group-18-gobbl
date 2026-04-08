import { useEffect, useState } from 'react'
import { toast } from 'sonner'
import { listDrivers, autoAssignDriver, assignDriver } from '../../features/delivery/deliveryApi'
import type { Driver } from '../../types'
import { getApiErrorMessage } from '../../utils/apiError'
import { Card } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { Input, Label } from '../../components/ui/Input'
import { StatusPill } from '../../components/ui/StatusPill'

export function OwnerDeliveryPage() {
  const [drivers, setDrivers] = useState<Driver[]>([])
  const [orderId, setOrderId] = useState('')
  const [busy, setBusy] = useState(false)

  async function refresh() {
    try {
      const res = await listDrivers()
      setDrivers(res.drivers)
    } catch (e) {
      toast.error(getApiErrorMessage(e))
    }
  }

  useEffect(() => {
    void refresh()
  }, [])

  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-extrabold text-gobbl-ink">Delivery management</h1>
      <Card>
        <Label htmlFor="oid">order_id</Label>
        <Input id="oid" className="mt-2 font-mono" value={orderId} onChange={(e) => setOrderId(e.target.value)} placeholder="uuid" />
        <div className="mt-4 flex flex-wrap gap-2">
          <Button
            disabled={!orderId || busy}
            onClick={async () => {
              setBusy(true)
              try {
                const res = (await autoAssignDriver(orderId)) as { message?: string }
                toast.success(res.message ?? 'Assigned')
                await refresh()
              } catch (e) {
                toast.error(getApiErrorMessage(e))
              } finally {
                setBusy(false)
              }
            }}
          >
            Auto-assign driver
          </Button>
        </div>
      </Card>

      <Card>
        <div className="mb-4 flex items-center justify-between gap-3">
          <h2 className="font-display text-lg font-bold">Drivers</h2>
          <Button variant="secondary" className="!py-2 !text-sm" onClick={() => void refresh()}>
            Refresh
          </Button>
        </div>
        <div className="grid gap-3 md:grid-cols-2">
          {drivers.map((d) => (
            <div key={d.driver_id} className="rounded-2xl border-2 border-white/80 bg-white/70 p-4">
              <div className="flex flex-wrap items-center gap-2">
                <p className="font-display text-xl font-bold">{d.name}</p>
                <StatusPill variant={d.status === 'available' ? 'success' : 'warning'}>{d.status}</StatusPill>
              </div>
              <p className="mt-2 text-sm text-gobbl-ink/70">driver_distance: {d.driver_distance}</p>
              <Button
                className="mt-4 w-full !py-2 !text-sm"
                variant="mint"
                disabled={!orderId || busy}
                onClick={async () => {
                  setBusy(true)
                  try {
                    const res = (await assignDriver(orderId, d.driver_id)) as { message?: string }
                    toast.success(res.message ?? 'Assigned')
                    await refresh()
                  } catch (e) {
                    toast.error(getApiErrorMessage(e))
                  } finally {
                    setBusy(false)
                  }
                }}
              >
                Assign to order
              </Button>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}
