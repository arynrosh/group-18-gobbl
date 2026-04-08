import type { Notification } from '../types'

/** Newest first: by timestamp when parseable, else by notification_id. */
export function sortNotificationsNewestFirst(items: Notification[]): Notification[] {
  return [...items].sort((a, b) => {
    const ta = Date.parse(a.timestamp)
    const tb = Date.parse(b.timestamp)
    const aOk = !Number.isNaN(ta)
    const bOk = !Number.isNaN(tb)
    if (aOk && bOk && tb !== ta) return tb - ta
    return b.notification_id - a.notification_id
  })
}
