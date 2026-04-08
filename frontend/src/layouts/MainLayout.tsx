import { Outlet } from 'react-router-dom'
import { motion } from 'framer-motion'
import { AppNav } from '../components/AppNav'

export function MainLayout() {
  return (
    <div className="flex min-h-screen flex-col">
      <AppNav />
      <motion.main
        className="mx-auto w-full max-w-6xl flex-1 px-4 py-8"
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.25 }}
      >
        <Outlet />
      </motion.main>
      <footer className="border-t-2 border-white/60 bg-white/50 py-6 text-center text-sm text-gobbl-ink/60">
        Gobbl demo frontend — wired to your FastAPI backend.
      </footer>
    </div>
  )
}
