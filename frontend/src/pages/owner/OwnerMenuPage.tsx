import { useEffect, useState } from 'react'
import { toast } from 'sonner'
import { browseRestaurants, fetchMenu } from '../../features/restaurants/restaurantApi'
import { createMenuItem, updateMenuItem, deleteMenuItem } from '../../features/menu/menuOwnerApi'
import type { MenuItem, Restaurant } from '../../types'
import { getApiErrorMessage } from '../../utils/apiError'
import { getOwnerRestaurantId, setOwnerRestaurantId } from '../../utils/ownerContext'
import { Card } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { Input, Label } from '../../components/ui/Input'
import { ConfirmDialog } from '../../components/ConfirmDialog'

export function OwnerMenuPage() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([])
  const [rid, setRid] = useState<number | ''>(() => getOwnerRestaurantId() ?? '')
  const [items, setItems] = useState<MenuItem[]>([])
  const [loading, setLoading] = useState(false)
  const [toDelete, setToDelete] = useState<MenuItem | null>(null)
  const [editing, setEditing] = useState<MenuItem | null>(null)

  const [restaurant_name, setRestaurantName] = useState('')
  const [cuisine, setCuisine] = useState('')
  const [food_item, setFoodItem] = useState('')
  const [order_value, setOrderValue] = useState('')

  useEffect(() => {
    void browseRestaurants(100, 0).then((r) => setRestaurants(r.items as Restaurant[]))
  }, [])

  useEffect(() => {
    if (rid === '' || !Number.isFinite(Number(rid))) {
      setItems([])
      return
    }
    let cancelled = false
    ;(async () => {
      setLoading(true)
      try {
        const m = await fetchMenu(Number(rid))
        if (!cancelled) setItems(m)
      } catch (e) {
        if (!cancelled) toast.error(getApiErrorMessage(e))
      } finally {
        if (!cancelled) setLoading(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [rid])

  function startCreate() {
    setEditing(null)
    setRestaurantName('')
    setCuisine('')
    setFoodItem('')
    setOrderValue('')
  }

  function startEdit(it: MenuItem) {
    setEditing(it)
    setRestaurantName(it.restaurant_name)
    setCuisine(it.cuisine)
    setFoodItem(it.food_item)
    setOrderValue(String(it.order_value))
  }

  const numericRid = rid === '' ? NaN : Number(rid)

  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-extrabold text-gobbl-ink">Menu management</h1>
      <Card>
        <Label htmlFor="rid">restaurant_id</Label>
        <div className="mt-2 flex flex-col gap-3 md:flex-row">
          <select
            id="rid"
            className="w-full rounded-2xl border-2 border-gobbl-peach/80 bg-white/90 px-4 py-3 font-semibold md:max-w-xs"
            value={rid === '' ? '' : String(rid)}
            onChange={(e) => {
              const v = e.target.value === '' ? '' : Number(e.target.value)
              setRid(v)
              if (typeof v === 'number' && Number.isFinite(v)) setOwnerRestaurantId(v)
            }}
          >
            <option value="">Select restaurant…</option>
            {restaurants.map((r) => (
              <option key={r.restaurant_id} value={r.restaurant_id}>
                {r.restaurant_name} (#{r.restaurant_id})
              </option>
            ))}
          </select>
          <Button
            type="button"
            variant="secondary"
            onClick={() => rid !== '' && setOwnerRestaurantId(Number(rid))}
          >
            Save selection locally
          </Button>
        </div>
      </Card>

      <Card>
        <h2 className="font-display text-lg font-bold">{editing ? 'Edit item' : 'Add item'}</h2>
        <form
          className="mt-4 grid gap-4 md:grid-cols-2"
          onSubmit={async (e) => {
            e.preventDefault()
            if (!Number.isFinite(numericRid)) {
              toast.error('Pick a restaurant_id first')
              return
            }
            try {
              if (editing) {
                await updateMenuItem(numericRid, editing.menu_item_id, {
                  restaurant_name,
                  cuisine,
                  food_item,
                  order_value: Number(order_value),
                })
                toast.success('Updated')
              } else {
                await createMenuItem(numericRid, {
                  restaurant_name,
                  cuisine,
                  food_item,
                  order_value: Number(order_value),
                })
                toast.success('Created')
              }
              setItems(await fetchMenu(numericRid))
              startCreate()
            } catch (err) {
              toast.error(getApiErrorMessage(err))
            }
          }}
        >
          <div>
            <Label htmlFor="rn">restaurant_name</Label>
            <Input id="rn" value={restaurant_name} onChange={(e) => setRestaurantName(e.target.value)} required />
          </div>
          <div>
            <Label htmlFor="cu">cuisine</Label>
            <Input id="cu" value={cuisine} onChange={(e) => setCuisine(e.target.value)} required />
          </div>
          <div>
            <Label htmlFor="fi">food_item</Label>
            <Input id="fi" value={food_item} onChange={(e) => setFoodItem(e.target.value)} required />
          </div>
          <div>
            <Label htmlFor="ov">order_value</Label>
            <Input id="ov" type="number" step="0.01" value={order_value} onChange={(e) => setOrderValue(e.target.value)} required />
          </div>
          <div className="flex flex-wrap gap-2 md:col-span-2">
            <Button type="submit">{editing ? 'Save changes' : 'Create item'}</Button>
            {editing && (
              <Button type="button" variant="ghost" onClick={startCreate}>
                Cancel edit
              </Button>
            )}
          </div>
        </form>
      </Card>

      <Card>
        <h2 className="font-display text-lg font-bold">Current menu</h2>
        {loading ? (
          <p className="mt-3 text-sm">Loading…</p>
        ) : (
          <ul className="mt-4 space-y-2">
            {items.map((it) => (
              <li
                key={it.menu_item_id}
                className="flex flex-wrap items-center justify-between gap-3 rounded-2xl bg-white/70 px-4 py-3 text-sm"
              >
                <div>
                  <p className="font-bold">
                    {it.food_item}{' '}
                    <span className="text-gobbl-tomato">${it.order_value.toFixed(2)}</span>
                  </p>
                  <p className="text-xs text-gobbl-ink/55">menu_item_id {it.menu_item_id}</p>
                </div>
                <div className="flex gap-2">
                  <Button variant="secondary" className="!py-2 !text-xs" type="button" onClick={() => startEdit(it)}>
                    Edit
                  </Button>
                  <Button variant="ghost" className="!py-2 !text-xs" type="button" onClick={() => setToDelete(it)}>
                    Delete
                  </Button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </Card>

      <ConfirmDialog
        open={!!toDelete}
        title="Delete menu item?"
        message="This calls DELETE /menu/{restaurant_id}/{menu_id}."
        onClose={() => setToDelete(null)}
        onConfirm={async () => {
          if (!toDelete || !Number.isFinite(numericRid)) return
          try {
            await deleteMenuItem(numericRid, toDelete.menu_item_id)
            toast.success('Deleted')
            setToDelete(null)
            setItems(await fetchMenu(numericRid))
          } catch (e) {
            toast.error(getApiErrorMessage(e))
          }
        }}
        danger
      />
    </div>
  )
}
