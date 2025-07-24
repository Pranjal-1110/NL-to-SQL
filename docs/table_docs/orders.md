 
---

# Table: orders

## Purpose
This table serves as the **core transactional record for sales**, capturing high-level details about each customer purchase, including customer, date, status, store, and staff information.

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `order_id` | int | A **unique numerical identifier** for each order. This column is the **primary key**. |
| `customer_id` | int | A **foreign key** linking this order to the specific customer who placed it. |
| `order_status` | int | An integer representing the **current status of the order** (e.g., `1=Pending`, `4=Completed`). |
| `order_date` | text | The **date when the order was placed**. |
| `required_date` | text | The **date by which the order is expected to be delivered**. (Nullable) |
| `shipped_date` | text | The **actual date when the order was shipped**. (Nullable) |
| `store_id` | int | A **foreign key** linking this order to the store location where it was placed. |
| `staff_id` | int | A **foreign key** linking this order to the staff member who handled it. (Nullable) |

## Relationships

**Connected to:**
- `customers` (via `customer_id`) - One customer can have many orders.
- `stores` (via `store_id`) - One store can have many orders.
- `staffs` (via `staff_id`) - One staff member can handle many orders.
- `order_items` (via `order_id`) - One order can contain multiple `order_items`.

---

