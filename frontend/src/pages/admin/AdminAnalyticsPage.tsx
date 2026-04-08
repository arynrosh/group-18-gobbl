import { useEffect, useState } from 'react'
import { toast } from 'sonner'
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { browseRestaurants } from '../../features/restaurants/restaurantApi'
import { getDeliveryTimes, getPopularByOrders, getPopularByRatings } from '../../features/admin/statisticsApi'
import type { Restaurant } from '../../types'
import { getApiErrorMessage } from '../../utils/apiError'
import { Card } from '../../components/ui/Card'
import { StatusPill } from '../../components/ui/StatusPill'

type DeliveryPayload = {
  per_restaurant?: Record<string, number>
  system_wide_average_minutes?: number | null
}

export function AdminAnalyticsPage() {
  const [delivery, setDelivery] = useState<DeliveryPayload | null>(null)
  const [byOrders, setByOrders] = useState<{ restaurant_id: number; total_orders?: number }[]>([])
  const [byRatings, setByRatings] = useState<{ restaurant_id: number; average_rating?: number }[]>([])
  const [names, setNames] = useState<Record<number, string>>({})

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      try {
        const [d, o, r, br] = await Promise.all([
          getDeliveryTimes() as Promise<DeliveryPayload>,
          getPopularByOrders(10) as Promise<{ restaurant_id: number; total_orders: number }[]>,
          getPopularByRatings(10) as Promise<{ restaurant_id: number; average_rating: number }[]>,
          browseRestaurants(200, 0),
        ])
        if (cancelled) return
        setDelivery(d)
        setByOrders(Array.isArray(o) ? o : [])
        setByRatings(Array.isArray(r) ? r : [])
        const map: Record<number, string> = {}
        ;(br.items as Restaurant[]).forEach((x) => {
          map[x.restaurant_id] = x.restaurant_name
        })
        setNames(map)
      } catch (e) {
        if (!cancelled) toast.error(getApiErrorMessage(e))
      }
    })()
    return () => {
      cancelled = true
    }
  }, [])

  const deliveryChart =
    delivery?.per_restaurant &&
    Object.entries(delivery.per_restaurant).map(([id, minutes]) => ({
      name: names[Number(id)] ?? `R${id}`,
      minutes,
    }))

  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-extrabold text-gobbl-ink">Analytics</h1>

      <Card>
        <div className="flex flex-wrap items-center gap-2">
          <h2 className="font-display text-lg font-bold">Delivery times</h2>
          <StatusPill variant="info">GET /statistics/delivery-times</StatusPill>
        </div>
        <p className="mt-2 text-sm text-gobbl-ink/70">
          System average:{' '}
          <span className="font-black text-gobbl-tomato">
            {delivery?.system_wide_average_minutes != null ? `${delivery.system_wide_average_minutes} min` : 'n/a'}
          </span>
        </p>
        {deliveryChart && deliveryChart.length > 0 ? (
          <div className="mt-6 h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={deliveryChart}>
                <CartesianGrid strokeDasharray="4 4" stroke="#ffd8bf" />
                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="minutes" fill="#ff5c4d" radius={[12, 12, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p className="mt-4 text-sm text-gobbl-ink/65">Not enough timed orders to chart.</p>
        )}
      </Card>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <h2 className="font-display text-lg font-bold">Popular by orders</h2>
          <p className="text-xs text-gobbl-ink/55">GET /statistics/popular-restaurants/orders</p>
          <ul className="mt-4 space-y-2 text-sm">
            {byOrders.map((row) => (
              <li key={row.restaurant_id} className="flex justify-between gap-3 rounded-xl bg-white/70 px-3 py-2">
                <span className="font-semibold">{names[row.restaurant_id] ?? `Restaurant ${row.restaurant_id}`}</span>
                <span className="font-black text-gobbl-tomato">{row.total_orders}</span>
              </li>
            ))}
            {byOrders.length === 0 && <li className="text-gobbl-ink/65">No data</li>}
          </ul>
        </Card>
        <Card>
          <h2 className="font-display text-lg font-bold">Popular by ratings</h2>
          <p className="text-xs text-gobbl-ink/55">GET /statistics/popular-restaurants/ratings</p>
          <ul className="mt-4 space-y-2 text-sm">
            {byRatings.map((row) => (
              <li key={row.restaurant_id} className="flex justify-between gap-3 rounded-xl bg-white/70 px-3 py-2">
                <span className="font-semibold">{names[row.restaurant_id] ?? `Restaurant ${row.restaurant_id}`}</span>
                <span className="font-black text-gobbl-mint">{row.average_rating?.toFixed?.(2) ?? row.average_rating}</span>
              </li>
            ))}
            {byRatings.length === 0 && <li className="text-gobbl-ink/65">No data</li>}
          </ul>
        </Card>
      </div>
    </div>
  )
}
