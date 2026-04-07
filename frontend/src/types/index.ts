/** Mirrors backend roles in `app/services/user_service.py` */
export type UserRole = 'customer' | 'restaurant_owner' | 'driver' | 'admin'

export interface UserInfo {
  username: string
  role: UserRole | string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  role: UserRole
}

export interface UserResponse {
  username: string
  email: string
  role: string
}

export interface Paginated<T> {
  items: T[]
  total: number
  limit: number
  offset: number
}

export interface Restaurant {
  restaurant_id: number
  restaurant_name: string
  cuisine: string
}

export interface MenuItem {
  menu_item_id: number
  restaurant_id: number
  restaurant_name: string
  cuisine: string
  food_item: string
  order_value: number
  customer_rating?: number | null
  rating_count?: number | null
  delivery_time_actual?: number | null
}

export interface OrderItem {
  menu_item_id: number
  food_item: string
  quantity: number
  order_value: number
}

export interface Order {
  order_id: string
  customer_id: string
  restaurant_id: number
  delivery_distance: number
  delivery_time: number | null
  assigned_driver_id: number | null
  items: OrderItem[]
  sent: boolean
}

export interface CostBreakdown {
  order_id: string
  subtotal: number
  tax: number
  delivery_fee: number
  total: number
}

export interface OrderStatusRecord {
  order_id: string
  current: string
  complete: boolean
}

export interface PaymentRequest {
  order_id: string
  cardholder_name: string
  card_number: string
  expiry: string
  cvv: string
  discount_code?: string | null
}

export interface PaymentResponse {
  order_id: string
  status: string
  message: string
  transaction_id: string
}

export interface PaymentRecord {
  transaction_id: string
  order_id: string
  amount: number
  status: string
  timestamp: string
}

export interface SavePaymentMethodRequest {
  cardholder_name: string
  card_number: string
  expiry: string
}

export interface PaymentMethodResponse {
  method_id: string
  cardholder_name: string
  last_four: string
  expiry: string
}

export interface Notification {
  notification_id: number
  order_id: string
  customer_id: string
  restaurant_id: number
  message: string
  status: string
  timestamp: string
}

export interface NotificationRequest {
  customer_id: string
  order_id?: string | null
  restaurant_id: number
  message: string
}

export interface DiscountResponse {
  code_id: string
  code: string
  percentage: number
  expiry: string
  assigned_to: string[]
  used_by: string[]
}

export interface CreateDiscountRequest {
  code: string
  percentage: number
  expiry: string
  assigned_to: string[]
}

export interface RecommendedItem {
  menu_item_id: number
  food_item: string
  cuisine: string
  restaurant_id: number
  restaurant_name: string
  order_value: number
  customer_rating?: number | null
}

export interface Driver {
  driver_id: number
  name: string
  status: string
  driver_distance: number
}

export interface ItemRatingInput {
  menu_item_id: number
  food_item: string
  customer_rating: number
}

export interface ReviewCreate {
  order_id: string
  food_temperature: string
  food_freshness: number
  packaging_quality: number
  food_condition: string
  item_ratings: ItemRatingInput[]
}

export interface ReviewableItem {
  menu_item_id: number
  food_item: string
  customer_rating: number | null
}
