# Task 4.1 - Database Table Design for Orders 

## 1. Orders Table

**Purpose**:
Stores order information for a customer.

### Columns:
- order_id (Primary Key)
- customer_id (Foreign Key to Users.user_id)
- restaurant_id (Foreign Key to Restaurants.restaurant_id)
- status (NOT NULL)
- total_price (NOT NULL)
- created_at
- updated_at

### Constraints:
- status must be one of: PENDING, CONFIRMED, PREPARING, COMPLETED, CANCELLED
- total_price must be greater than or equal to 0
- restaurant_id must reference an existing restaurant

## 2. Order Items Table

**Purpose**:
Stores individual menu items that belong to an order.

### Columns:
- order_item_id (Primary Key)
- order_id (Foreign Key to Orders.order_id)
- menu_item_id (Foreign Key to MenuItems.menu_item_id)
- quantity (NOT NULL)
- item_price (NOT NULL)

### Constraints:
- quantity must be greater than 0
- item_price must be greater than or equal to 0
- An order cannot contain duplicate menu_item_id entries
- If an order is deleted, its order items are also deleted

## 3. Order Status Tracking Table

**Purpose**:
Tracks changes to an order's status over time.

### Columns:
- status_id (Primary Key)
- order_id (Foreign Key to Orders.order_id)
- status (NOT NULL)
- updated_at

### Constraints:
- status must be one of: PENDING, CONFIRMED, PREPARING, COMPLETED, CANCELLED
- If an order is deleted, its status history is also deleted

## Relationships Summary:

- One Restaurant can have many Orders
- One Order can have many Order Items
- One Order can have many Status Updates
