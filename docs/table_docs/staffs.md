
---

# Table: staffs

## Purpose
This table stores **comprehensive information about all employees**, including personal details, contact information, employment status, assigned store, and reporting hierarchy. It's used for HR management and tracking.

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `staff_id` | `int` | A **unique numerical identifier** for each staff member. This column is the **primary key**. |
| `first_name` | `text` | The staff member's **first name**. |
| `last_name` | `text` | The staff member's **last name**. |
| `email` | `text` | The staff member's primary **email address**. |
| `phone` | `text` | The staff member's **contact phone number**. (Nullable) |
| `active` | `int` | An indicator (`1` = active, `0` = inactive) of the staff member's **current employment status**. |
| `store_id` | `int` | A **foreign key** linking this staff member to their **primary store location**. |
| `manager_id` | `int` | A **self-referencing foreign key** linking this staff member to their **direct manager's `staff_id`**. (Nullable for top-level managers) |

## Relationships

**Connected to:**
- `stores` (via `store_id`) - Many staff members can belong to one store.
- `orders` (via `staff_id`) - One staff member can handle many orders.
- `staffs` (via `manager_id` - self-referencing) - Establishes an organizational hierarchy (who reports to whom).

---

