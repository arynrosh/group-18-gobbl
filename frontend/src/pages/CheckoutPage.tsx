import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { toast } from 'sonner'
import { useCartStore } from '../store/cartStore'
import { useAuthStore, hasRole } from '../store/authStore'
import { fetchOrder, sendOrder } from '../features/orders/orderApi'
import { processPayment } from '../features/payments/paymentApi'
import { listPaymentMethods } from '../features/payment-methods/paymentMethodsApi'
import type { Order, PaymentMethodResponse } from '../types'
import { computeCostBreakdown } from '../utils/costBreakdown'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { OrderLineItemsTable } from '../components/OrderLineItemsTable'
import { Button } from '../components/ui/Button'
import { Input, Label } from '../components/ui/Input'
import { StatusPill } from '../components/ui/StatusPill'

/** Simulated PAN/CVV for saved-method checkout — backend still validates card shape; no API change. */
const SIMULATED_SAVED_CARD_NUMBER = '4242424242424242'
const SIMULATED_SAVED_CVV = '123'

export function CheckoutPage() {
  const navigate = useNavigate()
  const [params] = useSearchParams()
  const paramOid = params.get('orderId')
  const { orderId: cartOid, clear: clearCart } = useCartStore()
  const orderId = paramOid || cartOid
  const user = useAuthStore((s) => s.user)

  const [order, setOrder] = useState<Order | null>(null)
  const [methods, setMethods] = useState<PaymentMethodResponse[]>([])
  const [busy, setBusy] = useState(false)

  const [cardholder_name, setCardholderName] = useState('')
  const [card_number, setCardNumber] = useState('')
  const [expiry, setExpiry] = useState('')
  const [cvv, setCvv] = useState('')
  const [discount_code, setDiscountCode] = useState('')
  const [selectedSavedMethod, setSelectedSavedMethod] = useState<PaymentMethodResponse | null>(null)

  useEffect(() => {
    if (!orderId) return
    let cancelled = false
    ;(async () => {
      try {
        const [o, ms] = await Promise.all([
          fetchOrder(orderId),
          listPaymentMethods().catch(() => []),
        ])
        if (cancelled) return
        setOrder(o)
        setMethods(ms)
        setSelectedSavedMethod(ms[0] ?? null)
      } catch (e) {
        if (!cancelled) toast.error(getApiErrorMessage(e))
      }
    })()
    return () => {
      cancelled = true
    }
  }, [orderId])

  const cost = useMemo(() => (order ? computeCostBreakdown(order) : null), [order])

  if (!user || !hasRole(user, ['customer'])) {
    return <p className="text-gobbl-ink/75">Log in as a customer to checkout.</p>
  }

  if (!orderId) {
    return <p className="text-gobbl-ink/75">No order selected. Open your cart first.</p>
  }

  const canPay = Boolean(order && order.items.length > 0)

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <h1 className="font-display text-4xl font-extrabold text-gobbl-ink">Checkout</h1>
      <p className="text-sm text-gobbl-ink/65">
        Pay here first. After payment succeeds, your order is submitted to the restaurant. With a saved card, card
        fields are skipped (simulated checkout).
      </p>

      {order && (
        <Card>
          <div className="flex flex-wrap items-center gap-2">
            <StatusPill variant={order.sent ? 'success' : 'warning'}>
              {order.sent ? 'Sent to restaurant' : 'Not sent yet — completes after payment'}
            </StatusPill>
            <span className="font-mono text-xs">{order.order_id}</span>
          </div>
        </Card>
      )}

      {order && order.items.length > 0 && (
        <Card className="!border-gobbl-ink/10 !bg-white shadow-[0_1px_3px_rgba(45,42,50,0.08)]">
          <h2 className="font-display text-lg font-bold text-gobbl-ink">Items in this order</h2>
          <p className="mt-1 text-xs text-gobbl-ink/55">Quantity, unit price, and line total.</p>
          <div className="mt-4">
            <OrderLineItemsTable items={order.items} />
          </div>
        </Card>
      )}

      {cost && (
        <Card className="!border-gobbl-ink/10 !bg-white shadow-[0_1px_3px_rgba(45,42,50,0.08)]">
          <h2 className="font-display text-lg font-bold text-gobbl-ink">Totals</h2>
          <dl className="mt-4 overflow-hidden rounded-2xl border border-gobbl-ink/10 bg-white text-sm">
            <div className="flex items-center justify-between gap-4 border-b border-gobbl-ink/8 px-4 py-3">
              <dt className="text-gobbl-ink/65">Subtotal</dt>
              <dd className="tabular-nums font-semibold text-gobbl-ink">${cost.subtotal.toFixed(2)}</dd>
            </div>
            <div className="flex items-center justify-between gap-4 border-b border-gobbl-ink/8 px-4 py-3">
              <dt className="text-gobbl-ink/65">Tax</dt>
              <dd className="tabular-nums font-semibold text-gobbl-ink">${cost.tax.toFixed(2)}</dd>
            </div>
            <div className="flex items-center justify-between gap-4 border-b border-gobbl-ink/8 px-4 py-3">
              <dt className="text-gobbl-ink/65">Delivery</dt>
              <dd className="tabular-nums font-semibold text-gobbl-ink">${cost.delivery_fee.toFixed(2)}</dd>
            </div>
            <div className="flex items-center justify-between gap-4 bg-gobbl-ink/[0.02] px-4 py-3.5">
              <dt className="font-display text-base font-bold text-gobbl-ink">Total</dt>
              <dd className="tabular-nums font-display text-xl font-extrabold text-gobbl-ink">${cost.total.toFixed(2)}</dd>
            </div>
          </dl>
          <p className="mt-3 text-xs text-gobbl-ink/50">
            Discounts apply at payment — final charge may differ. See{' '}
            <code className="rounded border border-gobbl-ink/10 bg-gobbl-ink/[0.03] px-1">/payments/process</code>.
          </p>
        </Card>
      )}

      {methods.length > 0 && (
        <Card>
          <h2 className="font-display text-lg font-bold">Saved payment methods</h2>
          <p className="text-xs text-gobbl-ink/60">
            Choose a saved card to pay without typing card number or CVV (simulated gateway).
          </p>
          <ul className="mt-3 space-y-2">
            {methods.map((m) => (
              <li key={m.method_id}>
                <Button
                  variant={selectedSavedMethod?.method_id === m.method_id ? 'primary' : 'secondary'}
                  className="w-full !justify-start !py-2 !text-sm"
                  type="button"
                  onClick={() => setSelectedSavedMethod(m)}
                >
                  {m.cardholder_name} · •••• {m.last_four} · {m.expiry}
                </Button>
              </li>
            ))}
          </ul>
          <Button
            type="button"
            variant="ghost"
            className="mt-3 w-full !py-2 !text-sm text-gobbl-ink/70"
            onClick={() => {
              setSelectedSavedMethod(null)
              setCardholderName('')
              setCardNumber('')
              setExpiry('')
              setCvv('')
            }}
          >
            Use a different card (enter details below)
          </Button>
        </Card>
      )}

      <Card>
        <h2 className="font-display text-lg font-bold">Payment</h2>
        <form
          className="mt-4 space-y-4"
          onSubmit={async (e) => {
            e.preventDefault()
            if (!orderId || !canPay) return
            setBusy(true)
            try {
              const useSaved = selectedSavedMethod != null
              const res = await processPayment({
                order_id: orderId,
                cardholder_name: useSaved ? selectedSavedMethod.cardholder_name : cardholder_name,
                card_number: useSaved ? SIMULATED_SAVED_CARD_NUMBER : card_number.replace(/\s/g, ''),
                expiry: useSaved ? selectedSavedMethod.expiry : expiry,
                cvv: useSaved ? SIMULATED_SAVED_CVV : cvv,
                discount_code: discount_code.trim() || null,
              })
              try {
                const latest = await fetchOrder(orderId)
                if (!latest.sent) {
                  await sendOrder(orderId)
                }
                toast.success(res.message || 'Paid — order sent!')
              } catch (sendErr) {
                toast.error(
                  `Payment approved, but notifying the restaurant failed: ${getApiErrorMessage(sendErr)}`,
                )
              }
              clearCart()
              navigate(`/transactions/${encodeURIComponent(res.transaction_id)}`)
            } catch (err) {
              toast.error(getApiErrorMessage(err))
            } finally {
              setBusy(false)
            }
          }}
        >
          {selectedSavedMethod ? (
            <p className="rounded-2xl border border-gobbl-teal/30 bg-gobbl-teal/10 px-4 py-3 text-sm font-semibold text-gobbl-ink">
              Paying with saved card · •••• {selectedSavedMethod.last_four} · {selectedSavedMethod.expiry}
            </p>
          ) : null}
          <div
            className={`space-y-4 rounded-2xl transition-opacity ${
              selectedSavedMethod ? 'pointer-events-none opacity-45' : ''
            }`}
            aria-hidden={selectedSavedMethod != null}
          >
            <p className="text-xs font-bold uppercase tracking-wide text-gobbl-ink/45">
              {selectedSavedMethod ? 'Card details (not needed — using saved method)' : 'Card details'}
            </p>
            <div>
              <Label htmlFor="ch">cardholder_name</Label>
              <Input
                id="ch"
                value={cardholder_name}
                onChange={(e) => setCardholderName(e.target.value)}
                required={!selectedSavedMethod}
                disabled={!!selectedSavedMethod}
              />
            </div>
            <div>
              <Label htmlFor="cn">card_number (16 digits)</Label>
              <Input
                id="cn"
                inputMode="numeric"
                value={card_number}
                onChange={(e) => setCardNumber(e.target.value)}
                required={!selectedSavedMethod}
                disabled={!!selectedSavedMethod}
              />
            </div>
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <Label htmlFor="ex">expiry (MM/YY)</Label>
                <Input
                  id="ex"
                  placeholder="12/28"
                  value={expiry}
                  onChange={(e) => setExpiry(e.target.value)}
                  required={!selectedSavedMethod}
                  disabled={!!selectedSavedMethod}
                />
              </div>
              <div>
                <Label htmlFor="cvv">cvv</Label>
                <Input
                  id="cvv"
                  value={cvv}
                  onChange={(e) => setCvv(e.target.value)}
                  required={!selectedSavedMethod}
                  maxLength={4}
                  disabled={!!selectedSavedMethod}
                />
              </div>
            </div>
          </div>
          <div>
            <Label htmlFor="dc">discount_code (optional)</Label>
            <Input id="dc" value={discount_code} onChange={(e) => setDiscountCode(e.target.value)} />
          </div>
          <Button type="submit" className="w-full" disabled={!canPay || busy}>
            {busy ? 'Processing…' : 'Pay now'}
          </Button>
        </form>
      </Card>
    </div>
  )
}
