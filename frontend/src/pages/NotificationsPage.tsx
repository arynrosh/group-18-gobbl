import { useEffect, useMemo, useState } from 'react'
import { toast } from 'sonner'
import { useAuthStore, hasRole } from '../store/authStore'
import { getCustomerNotifications } from '../features/notifications/notificationApi'
import type { Notification } from '../types'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { StatusPill } from '../components/ui/StatusPill'
import { sortNotificationsNewestFirst } from '../utils/notificationsSort'

export function NotificationsPage() {
  const user = useAuthStore((s) => s.user)
  const [items, setItems] = useState<Notification[]>([])

  useEffect(() => {
    if (!user || !hasRole(user, ['customer'])) return
    let cancelled = false
    ;(async () => {
      try {
        const data = await getCustomerNotifications(user.username)
        if (!cancelled) setItems(data)
      } catch (e) {
        if (!cancelled) toast.error(getApiErrorMessage(e))
      }
    })()
    return () => {
      cancelled = true
    }
  }, [user])

  const sortedItems = useMemo(() => sortNotificationsNewestFirst(items), [items])

  if (!user || !hasRole(user, ['customer'])) {
    return <p className="text-gobbl-ink/75">Customers only.</p>
  }

  return (
    <div className="space-y-6">
      <h1 className="font-display text-4xl font-extrabold text-gobbl-ink">Notifications</h1>
      <p className="text-sm text-gobbl-ink/65">GET /notifications/customer/{'{customer_id}'} — uses JWT username as customer_id.</p>
      {sortedItems.length === 0 ? (
        <Card>
          <p className="text-lg font-semibold text-gobbl-ink/80">All quiet in the kitchen 🍳</p>
          <p className="mt-2 text-sm text-gobbl-ink/65">No notifications yet — place an order or ask an admin to send one.</p>
        </Card>
      ) : (
        <ul className="space-y-3">
          {sortedItems.map((n) => (
            <Card key={n.notification_id}>
              <div className="flex flex-wrap items-center gap-2">
                <StatusPill variant="info">{n.status}</StatusPill>
                <span className="text-xs font-mono text-gobbl-ink/55">#{n.notification_id}</span>
              </div>
              <p className="mt-3 font-semibold text-gobbl-ink">{n.message}</p>
              <p className="mt-2 text-xs text-gobbl-ink/55">
                order {n.order_id} · restaurant {n.restaurant_id} · {n.timestamp}
              </p>
            </Card>
          ))}
        </ul>
      )}
    </div>
  )
}
