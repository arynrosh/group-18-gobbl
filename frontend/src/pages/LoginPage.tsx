import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { toast } from 'sonner'
import { login } from '../features/auth/authApi'
import { useAuthStore } from '../store/authStore'
import { getApiErrorMessage } from '../utils/apiError'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input, Label } from '../components/ui/Input'

export function LoginPage() {
  const navigate = useNavigate()
  const loc = useLocation() as { state?: { from?: string } }
  const setToken = useAuthStore((s) => s.setToken)
  const fetchMe = useAuthStore((s) => s.fetchMe)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setBusy(true)
    try {
      const tok = await login(username, password)
      setToken(tok.access_token)
      await fetchMe()
      toast.success('Welcome back!')
      navigate(loc.state?.from && loc.state.from !== '/login' ? loc.state.from : '/', { replace: true })
    } catch (err) {
      toast.error(getApiErrorMessage(err, 'Login failed'))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="mx-auto max-w-md">
      <Card>
        <h1 className="font-display text-3xl font-extrabold text-gobbl-ink">Log in</h1>
        <p className="mt-1 text-sm text-gobbl-ink/70">Uses <code className="rounded bg-white/80 px-1">POST /auth/login</code> (form body).</p>
        <form className="mt-6 space-y-4" onSubmit={onSubmit}>
          <div>
            <Label htmlFor="u">Username</Label>
            <Input id="u" autoComplete="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
          </div>
          <div>
            <Label htmlFor="p">Password</Label>
            <Input
              id="p"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <Button type="submit" className="w-full" disabled={busy}>
            {busy ? 'Signing in…' : 'Sign in'}
          </Button>
        </form>
        <p className="mt-4 text-center text-sm text-gobbl-ink/70">
          New here?{' '}
          <Link className="font-bold text-gobbl-tomato hover:underline" to="/register">
            Register
          </Link>
        </p>
      </Card>
    </div>
  )
}
