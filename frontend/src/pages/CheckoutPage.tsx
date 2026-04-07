import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { toast } from 'sonner'
import { useCartStore } from '../store/cartStore'
import { useAuthStore, hasRole } from '../store/authStore'
import { fetchOrder, calculateCost } from '../features/orders/orderApi'
import { processPayment } from '../features/payments/paymentApi'
import { listPaymentMethods } from '../features/payment-methods/paymentMethodsApi'
import type { CostBreakdown, Order, PaymentMethodResponse } from '../types'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input, Label } from '../components/ui/Input'
import { StatusPill } from '../components/ui/StatusPill'

export function CheckoutPage() {
  const navigate = useNavigate()
  const [params] = useSearchParams()
  const paramOid = params.get('orderId')
  const { orderId: cartOid } = useCartStore()
  const orderId = paramOid || cartOid
  const user = useAuthStore((s) => s.user)

  const [order, setOrder] = useState<Order | null>(null)
  const [cost, setCost] = useState<CostBreakdown | null>(null)
  const [methods, setMethods] = useState<PaymentMethodResponse[]>([])
  const [busy, setBusy] = useState(false)

  const [cardholder_name, setCardholderName] = useState('')
  const [card_number, setCardNumber] = useState('')
  const [expiry, setExpiry] = useState('')
  const [cvv, setCvv] = useState('')
  const [discount_code, setDiscountCode] = useState('')

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
        try {
          const c = await calculateCost(orderId)
          if (!cancelled) setCost(c)
        } catch {
          if (!cancelled) setCost(null)
        }
      } catch (e) {
        if (!cancelled) toast.error(getApiErrorMessage(e))
      }
    })()
    return () => {
      cancelled = true
    }
  }, [orderId])

  if (!user || !hasRole(user, ['customer'])) {
    return <p className="text-gobbl-ink/75">Log in as a customer to checkout.</p>
  }

  if (!orderId) {
    return <p className="text-gobbl-ink/75">No order selected. Open your cart first.</p>
  }

  const canPay = order && order.sent && order.items.length > 0

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <h1 className="font-display text-4xl font-extrabold text-gobbl-ink">Checkout</h1>
      <p className="text-sm text-gobbl-ink/65">
        Backend requires a sent order with items before payment makes sense. Card fields map 1:1 to{' '}
        <code className="rounded bg-white/80 px-1">PaymentRequest</code>.
      </p>

      {order && (
        <Card>
          <div className="flex flex-wrap items-center gap-2">
            <StatusPill variant={order.sent ? 'success' : 'warning'}>{order.sent ? 'Sent' : 'Not sent'}</StatusPill>
            <span className="font-mono text-xs">{order.order_id}</span>
          </div>
          {!order.sent && (
            <p className="mt-3 text-sm text-gobbl-ink/75">Send your order from the cart page to unlock checkout.</p>
          )}
        </Card>
      )}

      {cost && (
        <Card>
          <h2 className="font-display text-lg font-bold">Totals</h2>
          <p className="mt-2 text-sm">
            Subtotal ${cost.subtotal.toFixed(2)} · Tax ${cost.tax.toFixed(2)} · Delivery ${cost.delivery_fee.toFixed(2)}
          </p>
          <p className="mt-1 text-2xl font-black text-gobbl-tomato">${cost.total.toFixed(2)}</p>
          <p className="mt-2 text-xs text-gobbl-ink/55">
            Note: live discount application happens server-side in <code className="rounded bg-white/70 px-1">/payments/process</code>{' '}
            — final charge may differ from this estimate.
          </p>
        </Card>
      )}

      {methods.length > 0 && (
        <Card>
          <h2 className="font-display text-lg font-bold">Saved methods (reference)</h2>
          <p className="text-xs text-gobbl-ink/60">
            The API does not attach a saved method id to processing — pick a card below as a reminder, then type details manually.
          </p>
          <ul className="mt-3 space-y-2">
            {methods.map((m) => (
              <li key={m.method_id}>
                <Button
                  variant="secondary"
                  className="w-full !justify-start !py-2 !text-sm"
                  type="button"
                  onClick={() => {
                    setCardholderName(m.cardholder_name)
                    setExpiry(m.expiry)
                    setCardNumber('')
                    setCvv('')
                    toast.message(`Prefilled name/expiry for card ending ${m.last_four}`)
                  }}
                >
                  {m.cardholder_name} · •••• {m.last_four} · {m.expiry}
                </Button>
              </li>
            ))}
          </ul>
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
              const res = await processPayment({
                order_id: orderId,
                cardholder_name,
                card_number: card_number.replace(/\s/g, ''),
                expiry,
                cvv,
                discount_code: discount_code.trim() || null,
              })
              toast.success(res.message || 'Paid!')
              navigate(`/transactions/${encodeURIComponent(res.transaction_id)}`)
            } catch (err) {
              toast.error(getApiErrorMessage(err))
            } finally {
              setBusy(false)
            }
          }}
        >
          <div>
            <Label htmlFor="ch">cardholder_name</Label>
            <Input id="ch" value={cardholder_name} onChange={(e) => setCardholderName(e.target.value)} required />
          </div>
          <div>
            <Label htmlFor="cn">card_number (16 digits)</Label>
            <Input id="cn" inputMode="numeric" value={card_number} onChange={(e) => setCardNumber(e.target.value)} required />
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <Label htmlFor="ex">expiry (MM/YY)</Label>
              <Input id="ex" placeholder="12/28" value={expiry} onChange={(e) => setExpiry(e.target.value)} required />
            </div>
            <div>
              <Label htmlFor="cvv">cvv</Label>
              <Input id="cvv" value={cvv} onChange={(e) => setCvv(e.target.value)} required maxLength={4} />
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
