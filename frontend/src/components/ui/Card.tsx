import clsx from 'clsx'
import type { HTMLAttributes, ReactNode } from 'react'

export function Card({
  className,
  children,
  hoverLift,
  ...rest
}: HTMLAttributes<HTMLDivElement> & { children: ReactNode; hoverLift?: boolean }) {
  return (
    <div
      className={clsx(
        'rounded-3xl border-2 border-white/70 bg-white/80 p-5 shadow-[0_12px_40px_-20px_rgba(45,42,50,0.35)] backdrop-blur-sm',
        hoverLift && 'transition hover:-translate-y-1 hover:shadow-[0_18px_50px_-18px_rgba(45,42,50,0.45)]',
        className,
      )}
      {...rest}
    >
      {children}
    </div>
  )
}
