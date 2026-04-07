import { useEffect } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { Toaster } from 'sonner'
import { useAuthStore } from './store/authStore'
import { MainLayout } from './layouts/MainLayout'
import { DashboardLayout } from './layouts/DashboardLayout'
import { ProtectedRoute } from './components/ProtectedRoute'
import { ErrorBoundary } from './components/ErrorBoundary'

import { HomePage } from './pages/HomePage'
import { LoginPage } from './pages/LoginPage'
import { RegisterPage } from './pages/RegisterPage'
import { NotFoundPage } from './pages/NotFoundPage'
import { RestaurantsPage } from './pages/RestaurantsPage'
import { RestaurantDetailPage } from './pages/RestaurantDetailPage'
import { CartPage } from './pages/CartPage'
import { CheckoutPage } from './pages/CheckoutPage'
import { OrderDetailPage } from './pages/OrderDetailPage'
import { OrderTrackPage } from './pages/OrderTrackPage'
import { TransactionPage } from './pages/TransactionPage'
import { PaymentMethodsPage } from './pages/PaymentMethodsPage'
import { MyDiscountsPage } from './pages/MyDiscountsPage'
import { NotificationsPage } from './pages/NotificationsPage'
import { ReviewOrderPage } from './pages/ReviewOrderPage'
import { RecommendationsPage } from './pages/RecommendationsPage'

import { OwnerDashboardPage } from './pages/owner/OwnerDashboardPage'
import { OwnerMenuPage } from './pages/owner/OwnerMenuPage'
import { OwnerDeliveryPage } from './pages/owner/OwnerDeliveryPage'
import { OwnerNotificationsPage } from './pages/owner/OwnerNotificationsPage'
import { OwnerOrdersPage } from './pages/owner/OwnerOrdersPage'

import { DriverDashboardPage } from './pages/driver/DriverDashboardPage'

import { AdminDashboardPage } from './pages/admin/AdminDashboardPage'
import { AdminDiscountsPage } from './pages/admin/AdminDiscountsPage'
import { AdminNotificationsPage } from './pages/admin/AdminNotificationsPage'
import { AdminAnalyticsPage } from './pages/admin/AdminAnalyticsPage'

function AuthBootstrap() {
  const fetchMe = useAuthStore((s) => s.fetchMe)
  useEffect(() => {
    void fetchMe()
  }, [fetchMe])
  return null
}

const ownerLinks = [
  { to: '/owner', label: 'Overview' },
  { to: '/owner/menu', label: 'Menu' },
  { to: '/owner/delivery', label: 'Delivery' },
  { to: '/owner/notifications', label: 'Alerts' },
  { to: '/owner/orders', label: 'Orders' },
]

const adminLinks = [
  { to: '/admin', label: 'Overview', end: true },
  { to: '/admin/discounts', label: 'Discount codes' },
  { to: '/admin/notifications', label: 'Notify' },
  { to: '/admin/analytics', label: 'Analytics' },
]

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <AuthBootstrap />
        <Toaster richColors position="top-center" />
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<HomePage />} />
            <Route path="login" element={<LoginPage />} />
            <Route path="register" element={<RegisterPage />} />
            <Route path="restaurants" element={<RestaurantsPage />} />
            <Route path="restaurants/:id" element={<RestaurantDetailPage />} />

            <Route element={<ProtectedRoute />}>
              <Route path="orders/:orderId" element={<OrderDetailPage />} />
              <Route path="transactions/:transactionId" element={<TransactionPage />} />
            </Route>

            <Route element={<ProtectedRoute roles={['customer']} />}>
              <Route path="cart" element={<CartPage />} />
              <Route path="checkout" element={<CheckoutPage />} />
              <Route path="orders/:orderId/track" element={<OrderTrackPage />} />
              <Route path="payment-methods" element={<PaymentMethodsPage />} />
              <Route path="discounts/my" element={<MyDiscountsPage />} />
              <Route path="notifications" element={<NotificationsPage />} />
              <Route path="reviews/order/:orderId" element={<ReviewOrderPage />} />
              <Route path="recommendations" element={<RecommendationsPage />} />
            </Route>

            <Route element={<ProtectedRoute roles={['restaurant_owner']} />}>
              <Route path="owner" element={<DashboardLayout title="Owner cockpit" links={ownerLinks} />}>
                <Route index element={<OwnerDashboardPage />} />
                <Route path="menu" element={<OwnerMenuPage />} />
                <Route path="delivery" element={<OwnerDeliveryPage />} />
                <Route path="notifications" element={<OwnerNotificationsPage />} />
                <Route path="orders" element={<OwnerOrdersPage />} />
              </Route>
            </Route>

            <Route element={<ProtectedRoute roles={['driver']} />}>
              <Route path="driver" element={<DriverDashboardPage />} />
            </Route>

            <Route element={<ProtectedRoute roles={['admin']} />}>
              {/* Explicit /admin prefix so nested screens (e.g. /admin/discounts) always match under this layout */}
              <Route path="/admin" element={<DashboardLayout title="Admin" links={adminLinks} />}>
                <Route index element={<AdminDashboardPage />} />
                <Route path="discounts" element={<AdminDiscountsPage />} />
                <Route path="notifications" element={<AdminNotificationsPage />} />
                <Route path="analytics" element={<AdminAnalyticsPage />} />
              </Route>
            </Route>

            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  )
}
