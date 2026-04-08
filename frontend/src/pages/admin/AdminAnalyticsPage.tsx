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
import { browseAllRestaurants } from '../../features/restaurants/restaurantApi'
import {
  fetchPopularOrderRows,
  fetchRestaurantsRankedByAggregatedReviewRatings,
} from '../../features/restaurants/popularRestaurants'
import { getDeliveryTimes } from '../../features/admin/statisticsApi'
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
  const [ready, setReady] = useState(false)

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      setReady(false)
      const [dRes, oRes, brRes, rankedRes] = await Promise.allSettled([
        getDeliveryTimes() as Promise<DeliveryPayload>,
        fetchPopularOrderRows(10),
        browseAllRestaurants(),
        fetchRestaurantsRankedByAggregatedReviewRatings(200, 10),
      ])
      if (cancelled) return

      if (dRes.status === 'fulfilled') {
        setDelivery(dRes.value)
      } else {
        toast.error(`Delivery times: ${getApiErrorMessage(dRes.reason)}`)
      }

      if (oRes.status === 'fulfilled') {
        setByOrders(oRes.value)
      } else {
        toast.error(`Popular by orders: ${getApiErrorMessage(oRes.reason)}`)
      }

      if (brRes.status === 'fulfilled') {
        const map: Record<number, string> = {}
        ;(brRes.value as Restaurant[]).forEach((x) => {
          map[x.restaurant_id] = x.restaurant_name
        })
        setNames(map)
      } else {
        toast.error(`Restaurant names: ${getApiErrorMessage(brRes.reason)}`)
      }

      if (rankedRes.status === 'fulfilled') {
        const ranked = rankedRes.value
        setByRatings(
          ranked.restaurants.map((r) => ({
            restaurant_id: r.restaurant_id,
            average_rating: ranked.ratingById[r.restaurant_id],
          })),
        )
      } else {
        toast.error(`Popular by ratings: ${getApiErrorMessage(rankedRes.reason)}`)
      }

      setReady(true)
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
      {!ready && <p className="text-sm text-gobbl-ink/60">Loading analytics…</p>}

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
                <span className="font-semibold">
                  {names[Number(row.restaurant_id)] ?? `Restaurant ${row.restaurant_id}`}
                </span>
                <span className="font-black text-gobbl-tomato">{row.total_orders}</span>
              </li>
            ))}
            {byOrders.length === 0 && <li className="text-gobbl-ink/65">No data</li>}
          </ul>
        </Card>
        <Card>
          <h2 className="font-display text-lg font-bold">Popular by ratings</h2>
          <p className="text-xs text-gobbl-ink/55">
            Average of all item stars in GET /reviews/restaurant/:id (submitted reviews), not menu-only averages.
          </p>
          <ul className="mt-4 space-y-2 text-sm">
            {byRatings.map((row) => (
              <li key={row.restaurant_id} className="flex justify-between gap-3 rounded-xl bg-white/70 px-3 py-2">
                <span className="font-semibold">
                  {names[Number(row.restaurant_id)] ?? `Restaurant ${row.restaurant_id}`}
                </span>
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
