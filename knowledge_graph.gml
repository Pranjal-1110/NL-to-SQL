graph [
  directed 1
  name "Database Schema Knowledge Graph"
  node [
    id 0
    label "brands"
  ]
  node [
    id 1
    label "categories"
  ]
  node [
    id 2
    label "customers"
  ]
  node [
    id 3
    label "order_items"
  ]
  node [
    id 4
    label "orders"
  ]
  node [
    id 5
    label "products"
  ]
  node [
    id 6
    label "staffs"
  ]
  node [
    id 7
    label "stocks"
  ]
  node [
    id 8
    label "stores"
  ]
  edge [
    source 3
    target 4
    predicate "references_order_id"
    on_column "order_id"
  ]
  edge [
    source 3
    target 5
    predicate "references_product_id"
    on_column "product_id"
  ]
  edge [
    source 4
    target 2
    predicate "references_customer_id"
    on_column "customer_id"
  ]
  edge [
    source 4
    target 6
    predicate "references_staff_id"
    on_column "staff_id"
  ]
  edge [
    source 4
    target 8
    predicate "references_store_id"
    on_column "store_id"
  ]
  edge [
    source 5
    target 0
    predicate "references_brand_id"
    on_column "brand_id"
  ]
  edge [
    source 5
    target 1
    predicate "references_category_id"
    on_column "category_id"
  ]
  edge [
    source 6
    target 8
    predicate "references_store_id"
    on_column "store_id"
  ]
  edge [
    source 6
    target 6
    predicate "references_manager_id"
    on_column "manager_id"
  ]
  edge [
    source 7
    target 8
    predicate "references_store_id"
    on_column "store_id"
  ]
  edge [
    source 7
    target 5
    predicate "references_product_id"
    on_column "product_id"
  ]
]
