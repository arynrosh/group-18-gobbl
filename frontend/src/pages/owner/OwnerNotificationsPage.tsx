import { useEffect, useState } from 'react'
import { toast } from 'sonner'
import { getRestaurantNotifications } from '../../features/notifications/notificationApi'
import type { Notification } from '../../types'
import { getApiErrorMessage } from '../../utils/apiError'
import { getOwnerRestaurantId, setOwnerRestaurantId } from '../../utils/ownerContext'
import { browseRestaurants } from '../../features/restaurants/restaurantApi'
import type { Restaurant } from '../../types'
import { Card } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { StatusPill } from '../../components/ui/StatusPill'

export function OwnerNotificationsPage() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([])
  const [rid, setRid] = useState<number | ''>(() => getOwnerRestaurantId() ?? '')
  const [items, setItems] = useState<Notification[]>([])
  const effectiveRid = rid === '' || !Number.isFinite(Number(rid)) ? null : Number(rid)

  useEffect(() => {
    void browseRestaurants(100, 0).then((r) => setRestaurants(r.items as Restaurant[]))
  }, [])

  useEffect(() => {
    if (effectiveRid === null) return
    let cancelled = false
    ;(async () => {
      try {
        const data = await getRestaurantNotifications(effectiveRid)
        if (!cancelled) setItems(data)
      } catch (e) {
        if (!cancelled) toast.error(getApiErrorMessage(e))
      }
    })()
    return () => {
      cancelled = true
    }
  }, [effectiveRid])

  const displayItems = effectiveRid === null ? [] : items

  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-extrabold text-gobbl-ink">Restaurant notifications</h1>
      <Card>
        <label className="mb-2 block text-sm font-bold">restaurant_id</label>
        <select
          className="w-full rounded-2xl border-2 border-gobbl-peach/80 bg-white/90 px-4 py-3 font-semibold"
          value={rid === '' ? '' : String(rid)}
          onChange={(e) => {
            const v = e.target.value === '' ? '' : Number(e.target.value)
            setRid(v)
            if (typeof v === 'number' && Number.isFinite(v)) setOwnerRestaurantId(v)
          }}
        >
          <option value="">Select…</option>
          {restaurants.map((r) => (
            <option key={r.restaurant_id} value={r.restaurant_id}>
              {r.restaurant_name} (#{r.restaurant_id})
            </option>
          ))}
        </select>
        <Button
          className="mt-4"
          variant="secondary"
          type="button"
          disabled={effectiveRid === null}
          onClick={async () => {
            if (effectiveRid === null) return
            try {
              setItems(await getRestaurantNotifications(effectiveRid))
            } catch (e) {
              toast.error(getApiErrorMessage(e))
            }
          }}
        >
          Reload
        </Button>
      </Card>
      {displayItems.length === 0 ? (
        <Card>
          <p className="text-gobbl-ink/70">No notifications for this restaurant yet.</p>
        </Card>
      ) : (
        <ul className="space-y-3">
          {displayItems.map((n) => (
            <Card key={n.notification_id}>
              <div className="flex flex-wrap gap-2">
                <StatusPill variant="info">{n.status}</StatusPill>
              </div>
              <p className="mt-3 font-semibold">{n.message}</p>
              <p className="mt-2 text-xs text-gobbl-ink/55">{n.timestamp}</p>
            </Card>
          ))}
        </ul>
      )}
    </div>
  )
}
