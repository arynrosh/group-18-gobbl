import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface CartState {
  orderId: string | null
  restaurantId: number | null
  deliveryDistance: number
  deliveryTime: number | null
  setSession: (p: {
    orderId: string
    restaurantId: number
    deliveryDistance?: number
    deliveryTime?: number | null
  }) => void
  patchDelivery: (p: { deliveryDistance?: number; deliveryTime?: number | null }) => void
  clear: () => void
}

export const useCartStore = create<CartState>()(
  persist(
    (set) => ({
      orderId: null,
      restaurantId: null,
      deliveryDistance: 5,
      deliveryTime: 30,
      setSession: ({ orderId, restaurantId, deliveryDistance, deliveryTime }) =>
        set((s) => ({
          orderId,
          restaurantId,
          deliveryDistance: deliveryDistance ?? s.deliveryDistance,
          deliveryTime: deliveryTime !== undefined ? deliveryTime : s.deliveryTime,
        })),
      patchDelivery: (p) => set((s) => ({ ...s, ...p })),
      clear: () =>
        set({
          orderId: null,
          restaurantId: null,
          deliveryDistance: 5,
          deliveryTime: 30,
        }),
    }),
    { name: 'gobbl-cart' },
  ),
)
