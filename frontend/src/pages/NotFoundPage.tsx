import { Link } from 'react-router-dom'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'

export function NotFoundPage() {
  return (
    <div className="mx-auto max-w-lg">
      <Card>
        <h1 className="font-display text-4xl font-black text-gobbl-tomato">404</h1>
        <p className="mt-2 text-lg font-semibold text-gobbl-ink">This page wandered off for a snack.</p>
        <Link to="/">
          <Button className="mt-6">Back home</Button>
        </Link>
      </Card>
    </div>
  )
}
