import { useEffect, useState } from 'react'
import { toast } from 'sonner'
import { updateDriverDistance, updateDriverStatus } from '../../features/delivery/deliveryApi'
import { getApiErrorMessage } from '../../utils/apiError'
import { getDriverId, setDriverId } from '../../utils/driverContext'
import { Card } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { Input, Label } from '../../components/ui/Input'
import { StatusPill } from '../../components/ui/StatusPill'

export function DriverDashboardPage() {
  const [driverId, setDid] = useState<number | ''>(() => getDriverId() ?? '')
  const [distance, setDistance] = useState('10')
  const [status, setStatus] = useState<'available' | 'busy'>('available')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    const id = getDriverId()
    if (id) setDid(id)
  }, [])

  const numericId = driverId === '' ? NaN : Number(driverId)

  return (
    <div className="mx-auto max-w-lg space-y-6">
      <h1 className="font-display text-3xl font-extrabold text-gobbl-ink">Driver desk</h1>
      <Card>
        <p className="text-sm text-gobbl-ink/70">
          The API updates drivers by numeric <span className="font-bold">driver_id</span> (see <code className="rounded bg-white/80 px-1">drivers.json</code>).
          There is no “who am I” endpoint — store your id locally for demos.
        </p>
        <div className="mt-4">
          <Label htmlFor="did">driver_id</Label>
          <Input
            id="did"
            type="number"
            value={driverId === '' ? '' : String(driverId)}
            onChange={(e) => {
              const v = e.target.value === '' ? '' : Number(e.target.value)
              setDid(v)
              if (typeof v === 'number' && Number.isFinite(v)) setDriverId(v)
            }}
          />
        </div>
      </Card>

      <Card>
        <h2 className="font-display text-lg font-bold">Update distance</h2>
        <p className="text-xs text-gobbl-ink/55">PUT /delivery/drivers/:id/driver_distance</p>
        <form
          className="mt-4 space-y-3"
          onSubmit={async (e) => {
            e.preventDefault()
            if (!Number.isFinite(numericId)) {
              toast.error('Set driver_id first')
              return
            }
            setBusy(true)
            try {
              await updateDriverDistance(numericId, Number(distance))
              toast.success('Distance updated')
            } catch (err) {
              toast.error(getApiErrorMessage(err))
            } finally {
              setBusy(false)
            }
          }}
        >
          <div>
            <Label htmlFor="dist">driver_distance</Label>
            <Input id="dist" type="number" step="0.1" value={distance} onChange={(e) => setDistance(e.target.value)} />
          </div>
          <Button type="submit" disabled={busy}>
            Save distance
          </Button>
        </form>
      </Card>

      <Card>
        <h2 className="font-display text-lg font-bold">Update status</h2>
        <p className="text-xs text-gobbl-ink/55">PUT /delivery/drivers/:id/driver_status — available | busy</p>
        <div className="mt-4 flex flex-wrap gap-2">
          <StatusPill variant={status === 'available' ? 'success' : 'warning'}>{status}</StatusPill>
        </div>
        <div className="mt-4 flex flex-wrap gap-2">
          {(['available', 'busy'] as const).map((s) => (
            <Button
              key={s}
              variant={status === s ? 'primary' : 'secondary'}
              type="button"
              className="!py-2 !text-sm"
              disabled={busy}
              onClick={() => setStatus(s)}
            >
              {s}
            </Button>
          ))}
        </div>
        <Button
          className="mt-4"
          disabled={busy || !Number.isFinite(numericId)}
          onClick={async () => {
            setBusy(true)
            try {
              await updateDriverStatus(numericId, status)
              toast.success('Status updated')
            } catch (err) {
              toast.error(getApiErrorMessage(err))
            } finally {
              setBusy(false)
            }
          }}
        >
          Save status
        </Button>
      </Card>
    </div>
  )
}
