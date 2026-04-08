import clsx from 'clsx'
import type { InputHTMLAttributes } from 'react'

export function Input({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={clsx(
        'w-full rounded-2xl border-2 border-gobbl-peach/80 bg-white/90 px-4 py-3 text-gobbl-ink outline-none transition focus:border-gobbl-mango focus:ring-2 focus:ring-gobbl-lemon/70',
        className,
      )}
      {...props}
    />
  )
}

export function Label({ children, htmlFor }: { children: React.ReactNode; htmlFor?: string }) {
  return (
    <label htmlFor={htmlFor} className="mb-1 block text-sm font-bold text-gobbl-ink/80">
      {children}
    </label>
  )
}
