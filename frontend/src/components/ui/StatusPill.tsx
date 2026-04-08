import clsx from 'clsx'

const tone: Record<string, string> = {
  default: 'bg-gobbl-peach text-gobbl-ink',
  success: 'bg-gobbl-mint/25 text-emerald-900 border border-gobbl-mint/40',
  warning: 'bg-gobbl-lemon/40 text-amber-900 border border-gobbl-mango/50',
  danger: 'bg-red-100 text-red-900 border border-red-200',
  info: 'bg-gobbl-teal/15 text-teal-900 border border-gobbl-teal/30',
}

export function StatusPill({
  children,
  variant = 'default',
  className,
}: {
  children: React.ReactNode
  variant?: keyof typeof tone
  className?: string
}) {
  return (
    <span
      className={clsx(
        'inline-flex items-center rounded-full px-3 py-1 text-xs font-extrabold uppercase tracking-wide',
        tone[variant] ?? tone.default,
        className,
      )}
    >
      {children}
    </span>
  )
}
