import type { CostBreakdown, Order } from '../types'

/** Mirrors app/services/cost_service.py (TAX_RATE, DELIVERY_FEE, rounding). */
export const COST_TAX_RATE = 0.13
export const COST_DELIVERY_FEE = 3.99

function round2(n: number): number {
  return Math.round(n * 100) / 100
}

/**
 * Same math as backend `calculate_cost` for a valid order. Use this when the
 * cost API cannot parse persisted orders (e.g. diet_restrictions shape) while
 * GET /orders still returns the raw document.
 */
export function computeCostBreakdown(order: Order): CostBreakdown {
  const subtotal = round2(
    order.items.reduce(
      (sum, it) => sum + (Number(it.order_value) || 0) * (Number(it.quantity) || 0),
      0,
    ),
  )
  const tax = round2(subtotal * COST_TAX_RATE)
  const total = round2(subtotal + tax + COST_DELIVERY_FEE)
  return {
    order_id: order.order_id,
    subtotal,
    tax,
    delivery_fee: COST_DELIVERY_FEE,
    total,
  }
}
