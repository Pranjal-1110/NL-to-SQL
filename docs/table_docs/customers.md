
---

# Table: customers

## Purpose
This table stores **detailed customer profile information**, including personal, contact, and address details. It's essential for managing customer relationships and processing orders.

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `customer_id` | int | A **unique numerical identifier** for each customer. This column is the **primary key**, linking customer records to their orders. |
| `first_name` | text | The **customer's first name**, used for personalization and identification. |
| `last_name` | text | The **customer's last name**, essential for identification and formal correspondence. |
| `phone` | text | The customer's primary **contact phone number**. (Nullable) |
| `email` | text | The customer's primary **email address**, a key communication channel. (Nullable) |
| `street` | text | The **street address** component of the customer's physical location, critical for shipping. |
| `city` | text | The **city** component of the customer's physical address, important for localized services. |
| `state` | text | The **state, province, or region** component of the customer's physical address (e.g., 'NY'), vital for shipping and regional analysis. |
| `zip_code` | int | The **postal code** corresponding to the customer's address, helping pinpoint location for delivery. |

## Relationships

**Connected to:**
- `orders` (via `customer_id`) - Establishes a one-to-many relationship where one customer can place multiple orders.

---
