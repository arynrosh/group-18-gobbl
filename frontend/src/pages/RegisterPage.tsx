import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { toast } from 'sonner'
import { register } from '../features/auth/authApi'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input, Label } from '../components/ui/Input'
import type { UserRole } from '../types'

const ROLES: { value: UserRole; label: string }[] = [
  { value: 'customer', label: 'Customer' },
  { value: 'restaurant_owner', label: 'Restaurant owner' },
  { value: 'driver', label: 'Driver' },
  { value: 'admin', label: 'Admin' },
]

export function RegisterPage() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState<UserRole>('customer')
  const [busy, setBusy] = useState(false)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setBusy(true)
    try {
      await register({ username, email, password, role })
      toast.success('Account created — you can log in now.')
      navigate('/login')
    } catch (err) {
      toast.error(getApiErrorMessage(err, 'Registration failed'))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="mx-auto max-w-md">
      <Card>
        <h1 className="font-display text-3xl font-extrabold text-gobbl-ink">Join Gobbl</h1>
        <p className="mt-1 text-sm text-gobbl-ink/70">Uses <code className="rounded bg-white/80 px-1">POST /users/register</code>.</p>
        <form className="mt-6 space-y-4" onSubmit={onSubmit}>
          <div>
            <Label htmlFor="username">Username</Label>
            <Input id="username" value={username} onChange={(e) => setUsername(e.target.value)} required minLength={3} />
          </div>
          <div>
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div>
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
            />
            <p className="mt-1 text-xs text-gobbl-ink/55">8+ chars and at least one number (backend rule).</p>
          </div>
          <div>
            <Label htmlFor="role">Role</Label>
            <select
              id="role"
              className="w-full rounded-2xl border-2 border-gobbl-peach/80 bg-white/90 px-4 py-3 font-semibold"
              value={role}
              onChange={(e) => setRole(e.target.value as UserRole)}
            >
              {ROLES.map((r) => (
                <option key={r.value} value={r.value}>
                  {r.label}
                </option>
              ))}
            </select>
          </div>
          <Button type="submit" className="w-full" disabled={busy}>
            {busy ? 'Creating…' : 'Create account'}
          </Button>
        </form>
        <p className="mt-4 text-center text-sm text-gobbl-ink/70">
          Already have an account?{' '}
          <Link className="font-bold text-gobbl-tomato hover:underline" to="/login">
            Log in
          </Link>
        </p>
      </Card>
    </div>
  )
}
