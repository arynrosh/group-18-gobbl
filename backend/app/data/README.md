# Database Table Design

## Restaurants
| Column | Type | Constraints |
|--------|------|-------------|
| restaurant_id | int | PRIMARY KEY |
| location | str | optional |
| is_active | bool | DEFAULT TRUE |

## Menus
| Column | Type | Constraints |
|--------|------|-------------|
| menu_id | str | PRIMARY KEY |
| restaurant_id | int | FOREIGN KEY -> Restaurant.restaurant_id |
| title | str | NOT NULL, UNIQUE per restaurant |
| is_active | bool | DEFAULT TRUE |

**Relationships:** One Restaurant -> Many Menus  
**On DELETE CASCADE:** If a restaurant is deleted, its menus are deleted

## Menu Items
| Column | Type | Constraints |
|--------|------|-------------|
| menu_item_id | str | PRIMARY KEY |
| menu_id | str | FOREIGN KEY -> Menu.menu_id |
| name | str | NOT NULL, UNIQUE per menu |
| price | float | NOT NULL, >= 0 |
| category | str | NOT NULL |
| is_available | bool | DEFAULT TRUE |

**Relationships:** One Menu -> Many Menu Items  
**On DELETE CASCADE:** If a menu is deleted, its items are deleted

## Relationships Summary
- One Restaurant -> Many Menus
- One Menu -> Many Menu Items