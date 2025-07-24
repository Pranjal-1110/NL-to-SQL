import os
import sys

# Add the parent directory to Python path FIRST
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from generate_db import get_vector_store
from retrieve_doc import get_doc_content, get_chunks
from connect_mysql import get_connection

# Initialize database connection
conn, cursor = get_connection()

# Get all table names
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()
table_names = [table[0] for table in tables]

# Define directory paths
doc_dir = "/home/pranjalgoyal/GenAI/assgn2/docs/table_docs"
db_dir = "/home/pranjalgoyal/GenAI/assgn2/db/table_db"

# Build a mapping of normalized filenames (without .md) to file paths
filename_map = {}
for file in os.listdir(doc_dir):
    if file.endswith(".md"):
        name_without_ext = os.path.splitext(file)[0].lower()
        filename_map[name_without_ext] = os.path.join(doc_dir, file)

# Iterate over the actual table names
for table_name in table_names:
    normalized_name = table_name.lower()

    if normalized_name in filename_map:
        file_path = filename_map[normalized_name]
        doc_content = get_doc_content(file_path)
        chunks = get_chunks(doc_content)

        # Init the vector store
        print(f"Processing: Table '{table_name}' from File '{file_path}'")
        vector_store = get_vector_store(table_name, db_dir)
        vector_store.add_documents(chunks, file_name=table_name)
    else:
        print(f"Warning: No file found for table '{table_name}'")
