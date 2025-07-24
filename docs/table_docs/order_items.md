
---

# Table: order_items

## Purpose
This table captures the **line-item details for each order**, specifying the products, quantities, prices, and discounts within an order. It's crucial for calculating order totals and analyzing product sales.

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `order_id` | int | A **foreign key** linking this item to the main `orders` table. Part of the **composite primary key**. |
| `item_id` | int | A **unique identifier for each item within a single order**. Part of the **composite primary key** (with `order_id`). |
| `product_id` | int | A **foreign key** linking this item to the specific product in the `products` table that was purchased. |
| `quantity` | int | The **number of units** of the specified product in this order item. |
| `list_price` | double | The **base price of a single unit** of the product at the time of order, before discounts. |
| `discount` | double | The **percentage of discount** applied to the `list_price` for this item (e.g., 0.10 for 10% off). |

## Relationships

**Connected to:**
- `orders` (via `order_id`) - Each `order_item` belongs to an `order`. (Many-to-one)
- `products` (via `product_id`) - Each `order_item` refers to a `product`. (Many-to-one)

---
