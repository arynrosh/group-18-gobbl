import { NavLink, Outlet } from 'react-router-dom'
import clsx from 'clsx'

const side = ({ isActive }: { isActive: boolean }) =>
  clsx(
    'block rounded-2xl px-4 py-3 text-sm font-extrabold',
    isActive ? 'bg-gobbl-tomato text-white shadow-md' : 'text-gobbl-ink/80 hover:bg-white/70',
  )

export function DashboardLayout({
  title,
  links,
}: {
  title: string
  links: { to: string; label: string; end?: boolean }[]
}) {
  return (
    <div className="grid gap-8 lg:grid-cols-[240px_1fr]">
      <aside className="h-fit rounded-3xl border-2 border-white/80 bg-white/70 p-4 shadow-lg backdrop-blur-sm">
        <h2 className="font-display mb-4 text-lg font-bold text-gobbl-ink">{title}</h2>
        <nav className="flex flex-col gap-1" aria-label={`${title} sections`}>
          {links.map((l) => (
            <NavLink key={l.to} to={l.to} end={l.end} className={side}>
              {l.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <div>
        <Outlet />
      </div>
    </div>
  )
}
