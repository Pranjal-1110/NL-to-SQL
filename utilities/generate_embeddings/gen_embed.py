import os
from generate_db import get_vector_store
from retrieve_doc import get_doc_content, get_chunks

dir  = "/home/pranjalgoyal/GenAI/assgn2/docs"
db_dir = "/home/pranjalgoyal/GenAI/assgn2/db"

for item in os.listdir(dir):
    item_path = os.path.join(dir, item)
    if os.path.isfile(item_path) and item_path.endswith(".md"):
        
        print(f"Processing file: {item_path}")
        doc_content = get_doc_content(item_path)
        chunks = get_chunks(doc_content)

        # Generate the database name and path
        file_name = os.path.splitext(item)[0].lower()
        db_name = file_name + "_db"
        db_path = os.path.join(db_dir, db_name)
        print(f"Creating vector store for: {file_name} at {db_path}")
        
        # Initialize the vector store
        vector_store = get_vector_store(file_name, db_path)
        vector_store.add_documents(chunks)
    else:
        print(f"Skipping non-file or non-md item: {item_path}")