import { Link, NavLink, useNavigate } from 'react-router-dom'
import clsx from 'clsx'
import { useAuthStore, hasRole } from '../store/authStore'
import { useCartStore } from '../store/cartStore'
import { Button } from './ui/Button'
import type { UserRole } from '../types'

const linkClass = ({ isActive }: { isActive: boolean }) =>
  clsx(
    'rounded-xl px-3 py-2 text-sm font-bold transition',
    isActive ? 'bg-white text-gobbl-tomato shadow-sm' : 'text-gobbl-ink/75 hover:bg-white/50',
  )

function RoleLinks({ role }: { role: string }) {
  const r = role as UserRole
  if (r === 'customer') {
    return (
      <>
        <NavLink to="/restaurants" className={linkClass}>
          Restaurants
        </NavLink>
        <NavLink to="/orders" className={linkClass}>
          My orders
        </NavLink>
        <NavLink to="/cart" className={linkClass}>
          Cart
        </NavLink>
        <NavLink to="/recommendations" className={linkClass}>
          For you
        </NavLink>
        <NavLink to="/discounts/my" className={linkClass}>
          My promos
        </NavLink>
        <NavLink to="/payment-methods" className={linkClass}>
          Cards
        </NavLink>
        <NavLink to="/notifications" className={linkClass}>
          Alerts
        </NavLink>
        <NavLink to="/diet-restrictions" className={linkClass}>
          Diet
        </NavLink>
      </>
    )
  }
  if (r === 'restaurant_owner') {
    return (
      <>
        <NavLink to="/owner" className={linkClass}>
          Owner hub
        </NavLink>
        <NavLink to="/owner/menu" className={linkClass}>
          Menu
        </NavLink>
        <NavLink to="/owner/delivery" className={linkClass}>
          Delivery
        </NavLink>
        <NavLink to="/owner/notifications" className={linkClass}>
          Restaurant alerts
        </NavLink>
        <NavLink to="/owner/orders" className={linkClass}>
          Orders
        </NavLink>
      </>
    )
  }
  if (r === 'driver') {
    return (
      <NavLink to="/driver" className={linkClass}>
        Driver desk
      </NavLink>
    )
  }
  if (r === 'admin') {
    return (
      <>
        <NavLink to="/admin/discounts" className={linkClass}>
          Discount codes
        </NavLink>
        <NavLink to="/admin" end className={linkClass}>
          Admin home
        </NavLink>
        <NavLink to="/admin/notifications" className={linkClass}>
          Notify
        </NavLink>
        <NavLink to="/admin/analytics" className={linkClass}>
          Analytics
        </NavLink>
      </>
    )
  }
  return null
}

export function AppNav() {
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()
  const orderId = useCartStore((s) => s.orderId)

  return (
    <header className="sticky top-0 z-40 border-b-2 border-white/60 bg-white/70 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-4 py-3">
        <Link to="/" className="font-display text-2xl font-extrabold tracking-tight text-gobbl-tomato">
          Gobbl
        </Link>
        <nav className="hidden flex-1 flex-wrap items-center justify-center gap-1 md:flex">
          <NavLink to="/" end className={linkClass}>
            Home
          </NavLink>
          {user && <RoleLinks role={user.role} />}
        </nav>
        <div className="flex items-center gap-2">
          {user && hasRole(user, ['customer']) && orderId && (
            <span className="hidden rounded-full bg-gobbl-lemon/50 px-3 py-1 text-xs font-bold text-gobbl-ink sm:inline">
              Cart active
            </span>
          )}
          {user ? (
            <>
              <span className="hidden text-sm font-semibold text-gobbl-ink/70 sm:inline">{user.username}</span>
              <Button
                variant="secondary"
                className="!py-2 !text-sm"
                onClick={() => {
                  logout()
                  navigate('/login')
                }}
              >
                Log out
              </Button>
            </>
          ) : (
            <>
              <Link to="/login">
                <Button variant="ghost" className="!py-2 !text-sm">
                  Log in
                </Button>
              </Link>
              <Link to="/register">
                <Button className="!py-2 !text-sm">Join</Button>
              </Link>
            </>
          )}
        </div>
      </div>
      {user && (
        <div className="flex gap-1 overflow-x-auto border-t border-white/50 px-4 py-2 md:hidden">
          <NavLink to="/" end className={linkClass}>
            Home
          </NavLink>
          <RoleLinks role={user.role} />
        </div>
      )}
    </header>
  )
}
