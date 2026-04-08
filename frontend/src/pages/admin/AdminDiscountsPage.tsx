import { useEffect, useState } from 'react'
import { toast } from 'sonner'
import { createDiscount, getAllDiscounts } from '../../features/discounts/discountApi'
import type { DiscountResponse } from '../../types'
import { getApiErrorMessage } from '../../utils/apiError'
import { Card } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { Input, Label } from '../../components/ui/Input'

export function AdminDiscountsPage() {
  const [items, setItems] = useState<DiscountResponse[]>([])
  const [code, setCode] = useState('')
  const [percentage, setPercentage] = useState('10')
  const [expiry, setExpiry] = useState('2099-12-31')
  const [assigned, setAssigned] = useState('')
  const [busy, setBusy] = useState(false)

  async function refresh() {
    try {
      setItems(await getAllDiscounts())
    } catch (e) {
      toast.error(getApiErrorMessage(e))
    }
  }

  useEffect(() => {
    void refresh()
  }, [])

  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-extrabold text-gobbl-ink">Discount management</h1>
      <Card>
        <h2 className="font-display text-lg font-bold">Create discount</h2>
        <p className="text-xs text-gobbl-ink/55">POST /discounts — assigned_to is a list of usernames (comma-separated).</p>
        <form
          className="mt-4 grid gap-4 md:grid-cols-2"
          onSubmit={async (e) => {
            e.preventDefault()
            setBusy(true)
            try {
              await createDiscount({
                code,
                percentage: Number(percentage),
                expiry,
                assigned_to: assigned
                  .split(',')
                  .map((s) => s.trim())
                  .filter(Boolean),
              })
              toast.success('Discount created')
              setCode('')
              await refresh()
            } catch (err) {
              toast.error(getApiErrorMessage(err))
            } finally {
              setBusy(false)
            }
          }}
        >
          <div>
            <Label htmlFor="c">code</Label>
            <Input id="c" value={code} onChange={(e) => setCode(e.target.value)} required />
          </div>
          <div>
            <Label htmlFor="p">percentage</Label>
            <Input id="p" type="number" step="0.1" value={percentage} onChange={(e) => setPercentage(e.target.value)} required />
          </div>
          <div className="md:col-span-2">
            <Label htmlFor="ex">expiry (YYYY-MM-DD)</Label>
            <Input id="ex" value={expiry} onChange={(e) => setExpiry(e.target.value)} required />
          </div>
          <div className="md:col-span-2">
            <Label htmlFor="as">assigned_to</Label>
            <Input id="as" value={assigned} onChange={(e) => setAssigned(e.target.value)} placeholder="alice, bob" />
          </div>
          <Button type="submit" disabled={busy}>
            Create
          </Button>
        </form>
      </Card>

      <Card>
        <div className="mb-3 flex items-center justify-between gap-3">
          <h2 className="font-display text-lg font-bold">All discounts</h2>
          <Button variant="secondary" className="!py-2 !text-sm" type="button" onClick={() => void refresh()}>
            Refresh
          </Button>
        </div>
        <div className="space-y-3">
          {items.map((d) => (
            <div key={d.code_id} className="rounded-2xl bg-white/70 px-4 py-3 text-sm">
              <p className="font-bold">
                {d.code} · {d.percentage}% · expires {d.expiry}
              </p>
              <p className="mt-1 text-xs text-gobbl-ink/60">assigned_to: {d.assigned_to.join(', ') || '—'}</p>
              <p className="text-xs text-gobbl-ink/60">used_by: {d.used_by.join(', ') || '—'}</p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}
