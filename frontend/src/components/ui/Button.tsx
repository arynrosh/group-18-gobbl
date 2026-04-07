import clsx from 'clsx'
import type { ButtonHTMLAttributes, ReactNode } from 'react'

const variants = {
  primary:
    'bg-gobbl-tomato text-white shadow-[0_4px_0_#d9483d] hover:brightness-105 active:translate-y-0.5 active:shadow-none',
  secondary:
    'bg-white text-gobbl-ink border-2 border-gobbl-peach shadow-[0_4px_0_#f5d4c0] hover:bg-gobbl-peach/40',
  ghost: 'bg-transparent text-gobbl-ink hover:bg-white/60',
  mint: 'bg-gobbl-mint text-white shadow-[0_4px_0_#2aa67d] hover:brightness-105',
}

export function Button({
  className,
  variant = 'primary',
  children,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: keyof typeof variants
  children: ReactNode
}) {
  return (
    <button
      type="button"
      className={clsx(
        'font-display inline-flex items-center justify-center gap-2 rounded-2xl px-5 py-3 text-base font-semibold transition disabled:cursor-not-allowed disabled:opacity-50',
        variants[variant],
        className,
      )}
      {...props}
    >
      {children}
    </button>
  )
}
