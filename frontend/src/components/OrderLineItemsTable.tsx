import type { ReactNode } from 'react'
import type { OrderItem } from '../types'

function lineTotal(it: OrderItem): number {
  return (Number(it.order_value) || 0) * (Number(it.quantity) || 0)
}

type Props = {
  items: OrderItem[]
  /** Optional row action (e.g. Remove). Header is visually hidden to avoid duplicating the button label. */
  renderAction?: (it: OrderItem) => ReactNode
}

export function OrderLineItemsTable({ items, renderAction }: Props) {
  const showAction = Boolean(renderAction)

  if (items.length === 0) {
    return <p className="text-sm text-gobbl-ink/60">No line items.</p>
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-gobbl-ink/10 bg-white/90">
      <table className="w-full min-w-[320px] border-collapse text-sm">
        <thead>
          <tr className="border-b border-gobbl-ink/10 bg-gobbl-ink/[0.02] text-left text-xs font-semibold uppercase tracking-wide text-gobbl-ink/50">
            <th scope="col" className="sr-only">
              Item
            </th>
            <th scope="col" className="w-14 px-2 py-2.5 text-right font-medium">
              Qty
            </th>
            <th scope="col" className="w-24 px-2 py-2.5 text-right font-medium">
              Unit price
            </th>
            <th scope="col" className="w-28 px-3 py-2.5 text-right font-medium">
              Line total
            </th>
            {showAction && (
              <th scope="col" className="sr-only">
                Actions
              </th>
            )}
          </tr>
        </thead>
        <tbody>
          {items.map((it) => (
            <tr key={`${it.menu_item_id}-${it.food_item}`} className="border-b border-gobbl-ink/5 last:border-b-0">
              <td className="px-3 py-3 font-semibold text-gobbl-ink">{it.food_item}</td>
              <td className="px-2 py-3 text-right tabular-nums text-gobbl-ink">{it.quantity}</td>
              <td className="px-2 py-3 text-right tabular-nums text-gobbl-ink">${Number(it.order_value).toFixed(2)}</td>
              <td className="px-3 py-3 text-right tabular-nums font-semibold text-gobbl-ink">${lineTotal(it).toFixed(2)}</td>
              {showAction && <td className="px-3 py-3 text-right align-middle">{renderAction?.(it)}</td>}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
