
---

# Table: stocks

## Purpose
This table serves as a critical **inventory management table**, recording the **current quantity of each product at each specific store location**. It provides real-time visibility into available stock levels.

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `store_id` | `int` | A **foreign key** identifying the **store location**. Part of the **composite primary key**. |
| `product_id` | `int` | A **foreign key** identifying the **product** whose stock is recorded. Part of the **composite primary key**. |
| `quantity` | `int` | The **current number of units** of the specified product available at the designated store. `0` indicates out of stock. |

## Relationships

**Connected to:**
- `stores` (via `store_id`) - Many stock entries can point to one store.
- `products` (via `product_id`) - Many stock entries can refer to one product.
- (Conceptually forms a many-to-many relationship between `stores` and `products`.)

---
