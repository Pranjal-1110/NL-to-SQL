from utilities.generate_embeddings.generate_db import get_vector_store
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from groq import Groq
from model import table_result, Knowledge_Graph, RelevantColumnsOutput
from utilities.prompts import prompt_lvl1 , seed_table_extraction_prompt, column_extraction_prompt, col_filter_prompt , query_generation_prompt
from dotenv import load_dotenv
import os

load_dotenv()

# ------------------------------------------RELEVANT CHUNKS---------------------------------------------

# Load the existing vector store (already contains embedded documents)
vector_store_lvl1 = get_vector_store("overview", "db/overview_db")

# Create a retriever
retriever = vector_store_lvl1.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 10})

# Run a test query
query = input(str("what is your query? \n"))
results = retriever.invoke(query)

# -----------------------------------EXTRACTION OF POSSIBLE TABLES-----------------------------------------

# Provide structured output for the table names for the levels ahead.
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
model2 = ChatGroq(model = "llama-3.3-70b-versatile")
llm = model.with_structured_output(table_result)

# prompt for level1 RAG
prompt_lvl1 = prompt_lvl1

# Create the final prompt for Level 1 RAG
final_prompt_lvl1 = ChatPromptTemplate.from_messages(
    [
        ("system", prompt_lvl1),
        ("human", "{context}"),
        ("human", "{question}"),
    ]
)
# Create the chain for Level 1 RAG
chain = final_prompt_lvl1 | llm

# Invoke the chain with the context and query
results_lvl1 = chain.invoke({
    "context": "\n\n".join(doc.page_content for doc in results),
    "question": query
})


#  Get the initial broad list of tables from Level 1
initial_table_names_from_level1 = results_lvl1.table_names


# -------------------------------------EXTRACTION OF SEED TABLES--------------------------------------------
#1 identify the seed table
seed_prompt = seed_table_extraction_prompt

# 2. Create the chain for seed table extraction
seed_chain = ChatPromptTemplate.from_messages(
    [
        ("system", seed_prompt),
        ("human", "Given list of broadly relevant tables:\n{broadly_relevant_tables}\n\nUser Query:\n{user_query}"),
    ]
) | llm

# 3. Invoke the chain to get the seed tables
extracted_seed_tables_pydantic = seed_chain.invoke({
    "broadly_relevant_tables": ", ".join(initial_table_names_from_level1), # Pass as a comma-separated string
    "user_query": query # Your original user query
})

#4 Extract the list of strings
seed_tables = extracted_seed_tables_pydantic.table_names

print("SEED TABLES:" , end = " ")
for table in seed_tables:
    print(table, end=", ")
    
print("\n")

# -----------------------------KNOWLEDGE GRAPH FOR TABLES------------------------------------------------
kg_file_path = "knowledge_graph.gml"
table_KG  = Knowledge_Graph.load_graph(kg_file_path)

complete_paths , path_list = table_KG.validate_path(seed_tables)
print("\n")
for path in path_list:
    print(path)
    
print("\n")
for path in complete_paths:
    print(path)
    
print("\n")

filtered_tables  = []
required_colums = []

for source , fk_key, target in path_list:
    
    if source not in filtered_tables:
        filtered_tables.append(source)
        
    required_colums.append(f"{source} refers {target} via the foreign_key: {fk_key}")
    
    if target not in filtered_tables:
        filtered_tables.append(target)

# -------------------------------LEVEL-2 RAG: EXTRACTION OF COLUMNS-----------------------------------------

def get_table_context(table_name:str , query:str) -> str:
    temp_vector_store = get_vector_store(table_name , "db/table_db")
    temp_retriever = temp_vector_store.as_retriever(
        search_type = "similarity",
        search_kwargs = {"k":7}
    )
    
    results = temp_retriever.invoke(query)
    result_doc = "\n\n".join(doc.page_content for doc in results)
    
    return result_doc

def get_chain(user_query:str):
    col_extract_prompt = column_extraction_prompt
    col_extract_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", column_extraction_prompt),
            ("human", "USER QUERY: {user_query}\n\nRELEVANT DOCUMENT:\n{relevant_chunks}")
        ]
    )
    col_extraction_chain = col_extract_prompt | model.with_structured_output(RelevantColumnsOutput)
    return col_extraction_chain

def get_results(curr_table: str, query: str):
    col_chain = get_chain(query)
    relevant_docs = get_table_context(curr_table, query)
    # print(relevant_docs)

    try:
        col_results = col_chain.invoke({
            "relevant_chunks": relevant_docs,
            "user_query": query
        })
        return col_results

    except Exception as e:
        print(f"[ERROR] Model failed for table: {curr_table}\n{e}")
        return RelevantColumnsOutput(relevant_columns=[])


# print(get_table_context("products" , query))

reasons = dict()
tables = []

for table in filtered_tables:
    print(f"Processing table {table}")
    results = get_results(table , query)    
    relevant_cols = results.relevant_columns
    
    if len(relevant_cols)  > 0:
        tables.append(table)
        
        
    
    for col in relevant_cols:
        if col.column_name is not None and col.column_name not in reasons:
            key_1 = f"{col.table_name}.{col.column_name} ({col.data_type})"
            reasons[key_1] = col.reason


print("\nTABLES REQUIRED:")
for table in tables:
    print(table)

col_docs  = []
print("\nCOLUMNS REQUIRED")
for key,value in reasons.items():
    print(f"{key} -->{value}")
    col_docs.append(f"{key} -->{value}")



filter_chain = ChatPromptTemplate.from_messages(
    [
        ("system" , col_filter_prompt),
        ("human" , "Please now provide the final list of truly relevant columns for this query.")
    ]
) | model.with_structured_output(RelevantColumnsOutput)

filter_results = filter_chain.invoke(
    {
        "user_query" : query,
        "relevant_columns" : "\n".join(col_doc for col_doc in col_docs)
    }
)

final_cols = []
print("\nRELEVANT COLUMNS")
for rel_col in filter_results.relevant_columns:
    final_cols.append(f"{rel_col.table_name}.{rel_col.column_name} ({rel_col.data_type}) -> {rel_col.reason}")
    print(f"{rel_col.table_name}.{rel_col.column_name} ({rel_col.data_type}) -> {rel_col.reason}")
        
        
# ------------------------------------- QUERY GENERATION---------------------------------------------

model3 = ChatGroq(model = "qwen-qwq-32b")
col_relationships = required_colums
final_query_chain = ChatPromptTemplate.from_messages(
    [
        ("system" , query_generation_prompt),
        ("human" , "USER QUERY:\n {user_query} \n\nRELEVANT TABLES:\n{tables} \n\nTABLE RELATIONSHIPS:\n{relationships} \n\nRELEVANT COLUMNS (with reasons):\n{columns}")
    ]
) | model3

final_query = final_query_chain.invoke(
    {
        "user_query":query,
        "tables" : " ".join(table for table in tables),
        "relationships" : " \n".join(rel for rel in col_relationships),
        "columns" : " \n".join(col for col in final_cols)
    }
)

print(final_query.content)




