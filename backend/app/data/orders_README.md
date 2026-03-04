# Orders Database Table Design

## Orders Table
| Column | Type | Constraints |
|--------|------|-------------|
| order_id | str | PRIMARY KEY |
| customer_id | str | FOREIGN KEY -> Users.user_id |
| restaurant_id | int | FOREIGN KEY -> Restaurants.restaurant_id |
| status | str | NOT NULL, one of: PENDING, CONFIRMED, PREPARING, COMPLETED, CANCELLED |
| total_price | float | NOT NULL, >= 0 |
| created_at | str | optional |
| updated_at | str | optional |

## Order Items Table
| Column | Type | Constraints |
|--------|------|-------------|
| order_item_id | str | PRIMARY KEY |
| order_id | str | FOREIGN KEY -> Orders.order_id |
| menu_item_id | str | FOREIGN KEY -> MenuItems.menu_item_id, UNIQUE per order |
| quantity | int | NOT NULL, > 0 |
| item_price | float | NOT NULL, >= 0 |

**On DELETE CASCADE:** If an order is deleted, its order items are deleted

## Order Status Tracking Table
| Column | Type | Constraints |
|--------|------|-------------|
| status_id | str | PRIMARY KEY |
| order_id | str | FOREIGN KEY -> Orders.order_id |
| status | str | NOT NULL, one of: PENDING, CONFIRMED, PREPARING, COMPLETED, CANCELLED |
| updated_at | str | optional |

**On DELETE CASCADE:** If an order is deleted, its status history is deleted

## Relationships Summary
- One Restaurant -> Many Orders
- One Order -> Many Order Items
- One Order -> Many Status Updates