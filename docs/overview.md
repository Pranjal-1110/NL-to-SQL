# Bike Store Database Overview

## 1. Database Summary
This database models the operations of a bike store, designed to manage various aspects of its business. Its primary purpose is to keep track of products, customer information, sales orders, inventory levels across different stores, and staff details. This allows for efficient management of sales, customer relationships, product catalog, and stock availability.

## 2. Table Summaries
Below is a brief explanation of each table, detailing the data it stores and how it relates to real-world entities within the bike store operations.

### a. brands
- **name** : brands
- **Description**: This table stores information about the different **manufacturers** and **brands** of products available in the bike store. It helps categorize products by their origin and **brand identity**. Use this table to **filter products by brand**, understand **brand associations**, or retrieve **brand names** for reporting.
- **Important fields**:
  - `brand_id` (Primary Key) – unique identifier for each brand, useful for **linking products** to their respective brands.
  - `brand_name` – the official name of the brand (e.g., **Trek**, **Specialized**, **Giant**), crucial for **brand-specific queries** and **displaying product information**.
- **Connects to**: Products (via `brand_id` in the `products` table) - enabling **brand-product relationships** and **product filtering by brand**.
- **Keywords**: manufacturer, brand, company, product line, brand identity, filter by brand, brand name lookup, product manufacturer.

### b. categories
- **name** : categories
- **Description**: This table holds data about the various **product classifications** or **types of merchandise** into which products are classified (e.g., **Mountain Bikes**, **Road Bikes**, **Accessories**, **Apparel**, **Gear**, **Parts**, **Components**). It helps organize the **product catalog** and facilitates **category-specific reporting** and **filtering by product type**. Use this for grouping products like 'Cycling Accessories'.
- **Important fields**:
  - `category_id` (Primary Key) – unique identifier for each **product classification** or category.
  - `category_name` – the name of the category (e.g., 'Electric Bikes', 'Kids' Bikes', **'Bicycle Accessories'**, **'Cycling Gear'**, **'Bike Parts'**), useful for **Browse products by type** or **analyzing sales by category**.
- **Connects to**: Products (via `category_id` in the `products` table) - allowing **categorization of products** and **filtering products by category**.
- **Keywords**: product type, classification, genre, grouping, filter by category, product classification, **accessories**, **gear**, **parts**, **components**, **clothing**, **equipment**, **bicycle accessories**, **cycling gear**.

### c. customers
- **name** : customers
- **Description**: This table stores comprehensive details about individual **customers** who interact with the bike store. It's essential for **customer relationship management (CRM)**, **marketing efforts**, and **order tracking**.
- **Important fields**:
  - `customer_id` (Primary Key) – unique identifier for each **customer account**.
  - `first_name`, `last_name` – the **customer's full name**, used for personalization and identification.
  - `phone`, `email` – **contact information** for communication, order updates, and marketing.
  - `street`, `city`, `state`, `zip_code` – **location details** for shipping, local marketing, and geographical analysis.
- **Connects to**: Orders (via `customer_id` in the `orders` table) - enabling the **tracking of customer orders** and **purchase history**.
- **Keywords**: client, buyer, patron, contact details, address, customer information, CRM, purchase history.

### d. order_items
- **name** : order_items
- **Description**: This table captures the individual **products** and their details that constitute each **sales order** placed by customers. It details **which products were part of an order**, their specific **quantities**, and **pricing information** including any discounts. This is crucial for **order fulfillment** and **revenue calculation**.
- **Important fields**:
  - `order_id` (Foreign Key) – links to the main **order record** in the `orders` table.
  - `item_id` (Primary Key) – unique identifier for each **line item within an order**, distinguishing individual product entries.
  - `product_id` (Foreign Key) – links to the specific **product** being ordered from the `products` table.
  - `quantity` – the **number of units** of the product ordered in this item.
  - `list_price` – the **price of the product at the time of order**, before any discounts.
  - `discount` – any **discount percentage** applied to this specific item, affecting the final price.
- **Connects to**:
    - Orders (via `order_id`): To associate line items with their parent **sales order**.
    - Products (via `product_id`): To retrieve details about the **specific product** in the order.
- **Keywords**: line item, order detail, product quantity, unit price, sales discount, itemized bill, order contents, product sales.

### e. orders
- **name** : orders
- **Description**: This table represents a single **purchase transaction** made by a customer at a specific store, handled by a specific staff member. It tracks the **lifecycle of an order** from placement to shipment.
- **Important fields**:
  - `order_id` (Primary Key) – unique identifier for each **sales transaction**.
  - `customer_id` (Foreign Key) – links to the **customer who placed the order**.
  - `order_status` – numerical code indicating the **current status of the order** (e.g., 1=Pending, 2=Processing, 3=Rejected, 4=Completed), vital for **order management**.
  - `order_date` - the **date the order was placed**, essential for **time-based queries (e.g., 'in 2020', 'last year', 'by month')**
  - `required_date`, `shipped_date` – important **dates related to the order lifecycle**, used for tracking delivery and order processing times.(e.g., 'in 2020', 'last year', 'by month')**
  - `store_id` (Foreign Key) – links to the **store location** where the order was placed or originated.
  - `staff_id` (Foreign Key) – links to the **staff member who handled** or was assigned to the order.
- **Connects to**:
    - Customers (via `customer_id`): To identify **who placed the order** and access customer contact details. Allows **joining orders with customer information**.
    - Staffs (via `staff_id`): To determine **which staff member processed** or is responsible for the order. Facilitates **staff performance analysis**.
    - Stores (via `store_id`): To know **where the order was placed**. Useful for **store-specific sales reports** and inventory management.
    - Order Items (via `order_id`): This is a crucial link to see **what products were part of the order**, their quantities, and specific pricing. Essential for **calculating order totals** and **product-level sales data**.
- **Keywords**: sales transaction, purchase, customer order, order tracking, order status, order date, delivery, fulfillment, store sales.

### f. products
-- **name** : products
- **Description**: This table contains detailed information about all the **bicycles** and related **merchandise** sold by the store. It is the central repository for **product catalog** data.
- **Important fields**:
  - `product_id` (Primary Key) – unique identifier for each **individual product item**.
  - `product_name` – the **name of the product** (e.g., 'Electra Townie Go! 8D EQ Step-Through'), used for display and search.
  - `brand_id` (Foreign Key) – links to the **brand** that manufactures the product.
  - `category_id` (Foreign Key) – links to the **category** the product belongs to.
  - `model_year` – the **year of the product model**, useful for inventory rotation and promotions.
  - `list_price` – the **standard selling price** of the product, before any discounts.
- **Connects to**:
    - Brands (via `brand_id`): To retrieve **brand information** for each product.
    - Categories (via `category_id`): To classify products into **categories**.
    - Order Items (via `product_id`): When a product is sold, it becomes an **order item**.
    - Stocks (via `product_id`): To track the **inventory levels** of each product at different stores.
- **Keywords**: bicycle, item, merchandise, catalog, product details, model, price, inventory item, stock keeping unit (SKU).

### g. staffs
- **name** : staffs
- **Description**: This table manages information about the **employees** working at the bike stores. It's used for **staff management**, **performance tracking**, and **organizational hierarchy**.
- **Important fields**:
  - `staff_id` (Primary Key) – unique identifier for each **employee**.
  - `first_name`, `last_name` – the **employee's full name**.
  - `email`, `phone` – **contact details** for staff members.
  - `active` – a flag (0 or 1) indicating whether the **staff member is currently active** or inactive.
  - `store_id` (Foreign Key) – links to the **store location** where the staff member is primarily employed.
  - `manager_id` (Foreign Key) – identifies their **direct manager** within the staff hierarchy, enabling **reporting structures** and team organization.
- **Connects to**:
    - Stores (via `store_id`): To identify **where staff members work**.
    - Orders (via `staff_id`): To track **which staff member handled specific orders**.
- **Keywords**: employee, associate, personnel, team member, contact, active status, store assignment, manager, hierarchy.

### h. stocks
- **name** : stocks
- **Description**: This table tracks the **quantity of each product available** at each individual store location. It represents the **current inventory levels** and is critical for **stock management** and **order fulfillment**.
- **Important fields**:
  - `store_id` (Foreign Key) – links to the specific **store location** holding the stock.
  - `product_id` (Foreign Key) – links to the **product** whose stock is being tracked.
  - `quantity` – the **number of units of the product currently in stock** at that specific store.
- **Connects to**:
    - Stores (via `store_id`): To identify **stock levels per store**.
    - Products (via `product_id`): To identify **stock levels per product**.
- **Keywords**: inventory, merchandise on hand, product availability, current stock, warehouse, quantity on hand, inventory level.

### i. stores
- **name** : stores
- **Description**: This table holds details for each **physical bike store location**. It's used for **store management**, **contact information**, and **geographical analysis of sales**.
- **Important fields**:
  - `store_id` (Primary Key) – unique identifier for each **store branch or location**.
  - `store_name` – the **official name of the store** (e.g., 'Santa Cruz Bikes', 'New York Bike Hub').
  - `phone`, `email` – **contact information** for the store.
  - `street`, `city`, `state`, `zip_code` – **physical address** details for the store location.
- **Connects to**:
    - Orders (via `store_id`): To record **where orders were placed**.
    - Staffs (via `store_id`): To identify **which staff work at which store**.
    - Stocks (via `store_id`): To track **inventory levels at each store**.
- **Keywords**: location, branch, retail outlet, shop, address, store contact, physical location, sales point.

## 3. Real-world Entity Relationships
The database is structured to reflect natural relationships between real-world entities in a bike store business:

- A member of the **customers** table places an order, which is recorded in the **orders** table. This allows for **tracking customer purchase history**.
- An order in the **orders** table is handled by a staff member from the **staffs** table, enabling **staff performance tracking** related to sales.
- An order in the **orders** table is placed at a specific store, recorded in the **stores** table, facilitating **store-specific sales analysis**.
- An order in the **orders** table contains one or more individual products, detailed in the **order_items** table, which allows for **itemized order breakdowns**.
- Each item in the **order_items** table refers to a specific product from the **products** table, linking sales data to **product details**.
- Products in the **products** table belong to a category in the **categories** table, allowing for **product classification** and **categorization of sales**.
- Products in the **products** table are manufactured by brands listed in the **brands** table, enabling **brand-specific product management**.
- Stores in the **stores** table employ staff members from the **staffs** table, organizing **human resources by location**.
- **Stores** hold **stocks** of various **products**, representing the **inventory levels** at each physical location.
- Members in the **staffs** table can have a `manager_id`, indicating a hierarchical relationship within the Staff entity itself, defining the **organizational structure**.

## 4. Data Usage Scenarios
This database can answer a wide range of business questions, including:

- How many orders did a specific customer place? (Involving `customers` and `orders` tables)
- What are the best-selling products by quantity or revenue? (Typically involves `products`, `order_items`, and potentially `orders` for dates)
- Which staff member processed the most orders in a given month? (Requires `staffs` and `orders` tables)
- What is the current stock level of a particular product at a specific store? (Relates `stocks`, `products`, and `stores` tables)
- Which customers are located in a certain city or state? (Primarily the `customers` table)
- What is the total revenue generated by each store? (Involves `stores`, `orders`, and `order_items` for calculation)
- How many products are in the 'Mountain Bikes' category? (Querying the `products` and `categories` tables)