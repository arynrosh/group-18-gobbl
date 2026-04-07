import { Button } from './ui/Button'

export function ConfirmDialog({
  open,
  title,
  message,
  confirmLabel = 'Yes, do it',
  cancelLabel = 'Cancel',
  onConfirm,
  onClose,
  danger,
}: {
  open: boolean
  title: string
  message: string
  confirmLabel?: string
  cancelLabel?: string
  onConfirm: () => void
  onClose: () => void
  danger?: boolean
}) {
  if (!open) return null
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4 backdrop-blur-sm">
      <div className="w-full max-w-md rounded-3xl border-2 border-white bg-gobbl-cream p-6 shadow-2xl">
        <h3 className="font-display text-xl font-bold text-gobbl-ink">{title}</h3>
        <p className="mt-2 text-gobbl-ink/80">{message}</p>
        <div className="mt-6 flex flex-wrap justify-end gap-3">
          <Button variant="secondary" onClick={onClose}>
            {cancelLabel}
          </Button>
          <Button variant={danger ? 'primary' : 'mint'} onClick={onConfirm}>
            {confirmLabel}
          </Button>
        </div>
      </div>
    </div>
  )
}
