
---

# Table: products

## Purpose
This table serves as the **master catalog for all items available for sale**, storing comprehensive information like name, brand, category, model year, and price. It's fundamental for inventory, sales, and product display.

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `product_id` | int | A **unique numerical identifier** for each distinct product. This column is the **primary key**. |
| `product_name` | text | The full descriptive **name of the product** (e.g., "Electra Townie Go! 8D EQ Step-Thru"). |
| `brand_id` | int | A **foreign key** linking this product to its specific brand in the `brands` table. |
| `category_id` | int | A **foreign key** linking this product to its specific category in the `categories` table. |
| `model_year` | int | The **manufacturing or release year** of the product model. This column is only relevant when the user is referring to the manufacturing date, otherwise skipping this column is the best option |
| `list_price` | double | The **standard, advertised selling price** of the product, before any discounts or taxes (currency typically USD). |

## Relationships

**Connected to:**
- `brands` (via `brand_id`) - Many products belong to one brand.
- `categories` (via `category_id`) - Many products belong to one category.
- `order_items` (via `product_id`) - One product can appear in many `order_items`.
- `stocks` (via `product_id`) - One product can have stock levels across multiple stores.

---

