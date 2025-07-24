# Table: brands

## Purpose
This table stores **unique product brand names** and their identifiers, acting as a lookup for manufacturers.

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-----------|
| `brand_id` | int | A **unique numerical identifier** for each distinct product brand. This column is the **primary key**, ensuring each brand is uniquely identified. |
| `brand_name` | text | The full, human-readable **name of the product brand** (e.g., "Trek Bikes", "Giant Bicycles"). This name is used for display and identification. |

## Relationships

**Connected to:**
- `products` (via `brand_id`) - Establishes a one-to-many relationship where one brand can have many products.

---

