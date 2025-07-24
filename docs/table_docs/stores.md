
---

# Table: stores

## Purpose
This table serves as a **master data table for physical bike store locations**, providing essential contact and address details. It's foundational for attributing sales, managing inventory, and localizing operations.

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `store_id` | `int` | A **unique numerical identifier** for each distinct store location. This column is the **primary key**. |
| `store_name` | `text` | The **official name of the store location** (e.g., "Brooklyn Bikes"). |
| `phone` | `text` | The primary **contact phone number for the store**. (Nullable) |
| `email` | `text` | The primary **email address for the store**. (Nullable) |
| `street` | `text` | The **street address** component of the store's physical location. |
| `city` | `text` | The **city** where the store is located. |
| `state` | `text` | The **state, province, or region** where the store is located (e.g., 'NY'). |
| `zip_code` | `int` | The **postal code or ZIP code** corresponding to the store's address. |

## Relationships

**Connected to:**
- `orders` (via `store_id`) - One store can process many orders.
- `stocks` (via `store_id`) - One store can hold inventory for many products.
- `staffs` (via `store_id`) - One store can employ many staff members.

---
