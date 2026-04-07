import { useEffect, useState } from 'react'
import { toast } from 'sonner'
import { useAuthStore, hasRole } from '../store/authStore'
import { listPaymentMethods, savePaymentMethod, deletePaymentMethod } from '../features/payment-methods/paymentMethodsApi'
import type { PaymentMethodResponse } from '../types'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input, Label } from '../components/ui/Input'
import { ConfirmDialog } from '../components/ConfirmDialog'

export function PaymentMethodsPage() {
  const user = useAuthStore((s) => s.user)
  const [items, setItems] = useState<PaymentMethodResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)
  const [del, setDel] = useState<PaymentMethodResponse | null>(null)

  const [cardholder_name, setCardholderName] = useState('')
  const [card_number, setCardNumber] = useState('')
  const [expiry, setExpiry] = useState('')

  async function refresh() {
    setLoading(true)
    try {
      setItems(await listPaymentMethods())
    } catch (e) {
      toast.error(getApiErrorMessage(e))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void refresh()
  }, [])

  if (!user || !hasRole(user, ['customer'])) {
    return <p className="text-gobbl-ink/75">This page is for customers.</p>
  }

  return (
    <div className="space-y-6">
      <h1 className="font-display text-4xl font-extrabold text-gobbl-ink">Saved cards</h1>
      <Card>
        <h2 className="font-display text-lg font-bold">Add method</h2>
        <form
          className="mt-4 grid gap-4 md:grid-cols-2"
          onSubmit={async (e) => {
            e.preventDefault()
            setBusy(true)
            try {
              await savePaymentMethod({
                cardholder_name,
                card_number: card_number.replace(/\s/g, ''),
                expiry,
              })
              toast.success('Saved')
              setCardholderName('')
              setCardNumber('')
              setExpiry('')
              await refresh()
            } catch (err) {
              toast.error(getApiErrorMessage(err))
            } finally {
              setBusy(false)
            }
          }}
        >
          <div className="md:col-span-2">
            <Label htmlFor="ch">cardholder_name</Label>
            <Input id="ch" value={cardholder_name} onChange={(e) => setCardholderName(e.target.value)} required />
          </div>
          <div>
            <Label htmlFor="cn">card_number</Label>
            <Input id="cn" value={card_number} onChange={(e) => setCardNumber(e.target.value)} required />
          </div>
          <div>
            <Label htmlFor="ex">expiry</Label>
            <Input id="ex" placeholder="MM/YY" value={expiry} onChange={(e) => setExpiry(e.target.value)} required />
          </div>
          <div className="md:col-span-2">
            <Button type="submit" disabled={busy}>
              Save card
            </Button>
          </div>
        </form>
      </Card>

      <Card>
        <h2 className="font-display text-lg font-bold">Your methods</h2>
        {loading ? (
          <p className="mt-3 text-sm text-gobbl-ink/65">Loading…</p>
        ) : items.length === 0 ? (
          <p className="mt-3 text-sm text-gobbl-ink/65">No saved methods yet.</p>
        ) : (
          <ul className="mt-4 space-y-3">
            {items.map((m) => (
              <li key={m.method_id} className="flex flex-wrap items-center justify-between gap-3 rounded-2xl bg-white/70 px-4 py-3">
                <div>
                  <p className="font-bold">
                    {m.cardholder_name} · •••• {m.last_four}
                  </p>
                  <p className="text-xs text-gobbl-ink/60">{m.expiry}</p>
                </div>
                <Button variant="secondary" className="!py-2 !text-sm" onClick={() => setDel(m)}>
                  Delete
                </Button>
              </li>
            ))}
          </ul>
        )}
      </Card>

      <ConfirmDialog
        open={!!del}
        title="Delete saved card?"
        message="This cannot be undone in the UI."
        onClose={() => setDel(null)}
        onConfirm={async () => {
          if (!del) return
          setBusy(true)
          try {
            await deletePaymentMethod(del.method_id)
            toast.success('Deleted')
            setDel(null)
            await refresh()
          } catch (e) {
            toast.error(getApiErrorMessage(e))
          } finally {
            setBusy(false)
          }
        }}
        danger
      />
    </div>
  )
}
