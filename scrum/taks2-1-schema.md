# Task 2.1 - Database Table Design 

This document defines the database tables and constraints for:
- Restaurants
- Menus
- Menu Items

## 1. Restaurants Table
**Purpose:** Stores restaurant information.

### columns
-restaurant_id(primary key)
-name( NOT NULL)
-address (NOT NULL)
-phone
-is_active(default TRUE)
-created_at

### Constraints
-UNIQUE(name, adress)
-name cannot be empty 
-address cannot be empty

## 2. Menus Table 
**Purpose:** Each restauraunt can have multiple menus ( e.g., Lunch, Dinner). 

### Columns
- menu_id (primary key)
- restaurant_id ( Foreign_key -> Restaurants.restaurant_id)
- title (NOT NULL)
- is_active ( default TRUE)
- created_at

### Contraints
- UNIQUE (restaurant_id, title)
- On DELETE CASCADE ( if a restaurant is deleted, its menus are deleted)

## 3. Menu Items Table 
**Purpose:**Stores individual items belonging to a menu. 

### Columns
- menu_item_id (Primary key)
- menu_id (Foreign key -> Menus.menu_id)
- name (NOT NULL)
- description
- price (NOT NULL)
- category (NOT NULL)
- is_available ( default TRUE)
- created_at

  ### Constarints
  - UNIQUE (menu_id, name)
  - price must be >= 0
  - ON DELETE CASCADE (if a menu is deleted, its items are deleted)

## relationships summary
- one Restauraunt -> Many menus
- One menu -> Many Menu Items
