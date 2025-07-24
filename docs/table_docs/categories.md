
---

# Table: categories

## Purpose
This table defines and stores **product categories**, used to organize products into logical groups for Browse and management.

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `category_id` | int | A **unique numerical identifier** for each distinct product category. This column is the **primary key**, ensuring each category is uniquely identified. |
| `category_name` | text | The descriptive **name of the product category** (e.g., "Mountain Bikes", "Road Bikes", "Accessories"). This name is used for display and product classification. |

## Relationships

**Connected to:**
- `products` (via `category_id`) - Establishes a one-to-many relationship where one category can include many products.

---