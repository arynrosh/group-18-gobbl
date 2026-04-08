import { Component, type ErrorInfo, type ReactNode } from 'react'
import { Button } from './ui/Button'

export class ErrorBoundary extends Component<{ children: ReactNode }, { error?: Error }> {
  state: { error?: Error } = {}

  static getDerivedStateFromError(error: Error) {
    return { error }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error(error, info)
  }

  render() {
    if (this.state.error) {
      return (
        <div className="mx-auto flex min-h-[50vh] max-w-lg flex-col items-center justify-center gap-4 p-6 text-center">
          <h1 className="font-display text-3xl font-bold text-gobbl-tomato">Whoops — a little spill!</h1>
          <p className="text-gobbl-ink/80">{this.state.error.message}</p>
          <Button onClick={() => window.location.reload()}>Reload the app</Button>
        </div>
      )
    }
    return this.props.children
  }
}
