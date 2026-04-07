import { api } from '../../api/client'
import type { Driver } from '../../types'

export async function listDrivers(): Promise<{ drivers: Driver[] }> {
  const { data } = await api.get<{ drivers: Driver[] }>('/delivery/drivers')
  return data
}

export async function updateDriverDistance(driverId: number, driver_distance: number): Promise<{ driver: Driver }> {
  const { data } = await api.put(`/delivery/drivers/${driverId}/driver_distance`, { driver_distance })
  return data
}

export async function updateDriverStatus(driverId: number, status: string): Promise<{ driver: Driver }> {
  const { data } = await api.put(`/delivery/drivers/${driverId}/driver_status`, { status })
  return data
}

export async function autoAssignDriver(orderId: string): Promise<unknown> {
  const { data } = await api.post(`/delivery/orders/${orderId}/auto-assign-driver`)
  return data
}

export async function assignDriver(orderId: string, driverId: number): Promise<unknown> {
  const { data } = await api.post(`/delivery/orders/${orderId}/assign/${driverId}`)
  return data
}
