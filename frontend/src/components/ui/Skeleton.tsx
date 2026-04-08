import clsx from 'clsx'

export function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={clsx(
        'animate-pulse rounded-2xl bg-gradient-to-r from-gobbl-peach/50 via-white to-gobbl-peach/50',
        className,
      )}
    />
  )
}
