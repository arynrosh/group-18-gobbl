import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuthStore, hasRole } from '../store/authStore'
import type { UserRole } from '../types'

export function ProtectedRoute({ roles }: { roles?: UserRole[] }) {
  const { token, user, bootstrapped } = useAuthStore()
  const loc = useLocation()

  if (!bootstrapped) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <div className="font-display text-lg font-semibold text-gobbl-ink/70">Loading your session…</div>
      </div>
    )
  }

  if (!token) {
    return <Navigate to="/login" replace state={{ from: loc.pathname }} />
  }

  if (roles && !hasRole(user, roles)) {
    return <Navigate to="/" replace />
  }

  return <Outlet />
}
