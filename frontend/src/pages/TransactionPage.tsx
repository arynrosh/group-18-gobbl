import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { toast } from 'sonner'
import { getPaymentByTransaction } from '../features/payments/paymentApi'
import type { PaymentRecord } from '../types'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { StatusPill } from '../components/ui/StatusPill'
import { Skeleton } from '../components/ui/Skeleton'

export function TransactionPage() {
  const { transactionId } = useParams()
  const [p, setP] = useState<PaymentRecord | null | 'loading'>('loading')

  useEffect(() => {
    if (!transactionId) return
    let cancelled = false
    ;(async () => {
      try {
        const data = await getPaymentByTransaction(transactionId)
        if (!cancelled) setP(data)
      } catch (e) {
        if (!cancelled) {
          setP(null)
          toast.error(getApiErrorMessage(e))
        }
      }
    })()
    return () => {
      cancelled = true
    }
  }, [transactionId])

  if (p === 'loading') {
    return <Skeleton className="h-40" />
  }

  if (!p) {
    return (
      <Card>
        <p className="text-gobbl-ink/75">Transaction not found.</p>
        <Link to="/">
          <Button className="mt-4">Home</Button>
        </Link>
      </Card>
    )
  }

  return (
    <div className="mx-auto max-w-lg space-y-6">
      <h1 className="font-display text-4xl font-extrabold text-gobbl-ink">Payment receipt</h1>
      <Card>
        <div className="flex flex-wrap items-center gap-2">
          <StatusPill variant="success">{p.status}</StatusPill>
          <span className="font-mono text-xs break-all">{p.transaction_id}</span>
        </div>
        <dl className="mt-4 space-y-2 text-sm">
          <div className="flex justify-between gap-4">
            <dt className="text-gobbl-ink/60">order_id</dt>
            <dd className="font-mono font-bold">{p.order_id}</dd>
          </div>
          <div className="flex justify-between gap-4">
            <dt className="text-gobbl-ink/60">amount</dt>
            <dd className="font-black text-gobbl-tomato">${p.amount.toFixed(2)}</dd>
          </div>
          <div className="flex justify-between gap-4">
            <dt className="text-gobbl-ink/60">timestamp</dt>
            <dd className="font-semibold">{p.timestamp}</dd>
          </div>
        </dl>
        <Link to="/orders">
          <Button className="mt-6 w-full" variant="mint">
            View my orders
          </Button>
        </Link>
      </Card>
    </div>
  )
}
