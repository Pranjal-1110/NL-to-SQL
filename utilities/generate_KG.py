import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import Knowledge_Graph
from connect_mysql import get_connection

# Import nodes from the database
conn , cursor = get_connection()
cursor.execute("show tables;")
tables = cursor.fetchall()

nodes = [table[0] for table in tables]

fk_edges = [
    # orders table FKs
    ("orders", "customers", "customer_id"),
    ("orders", "staffs", "staff_id"),
    ("orders", "stores", "store_id"),

    # order_items table FKs
    ("order_items", "orders", "order_id"),
    ("order_items", "products", "product_id"),

    # products table FKs
    ("products", "brands", "brand_id"),
    ("products", "categories", "category_id"),

    # staffs table FKs
    ("staffs", "stores", "store_id"),
    ("staffs", "staffs", "manager_id"),

    # stocks table FKs
    ("stocks", "stores", "store_id"),
    ("stocks", "products", "product_id"),
]

table_KG = Knowledge_Graph(
    table_names=nodes,
    fk_relationships= fk_edges,
)

table_KG.draw_graph()
table_KG.save_graph("/home/pranjalgoyal/GenAI/assgn2/knowledge_graph.gml")
               

