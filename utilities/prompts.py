prompt_lvl1 = """

As an expert database schema analyst, your **PRIMARY GOAL** is to identify **ALL POTENTIALLY RELEVANT SQL table names** from the provided database context that *could possibly be needed or useful* to answer the user's query.

**Prioritize maximum recall and inclusion at this stage.** Do NOT filter for exact relevance or optimal SQL join paths; that comes later. If a table's description or its relationship to other tables contains any terms or concepts that *might* relate to the query, **INCLUDE IT**. Think broadly about all entities involved.

**Specifically, if a brand name, store name, category, or specific date/year is mentioned, ensure the corresponding lookup tables (like 'brands', 'stores', 'categories', or tables with date columns like 'orders') are included if their chunks were provided.**

List **ALL** potentially relevant table names identified from the context (return ONLY the table names as a list, e.g., ["table1", "table2", "table3"]):

"""

seed_table_extraction_prompt = """

You are an expert database schema analyst. Your task is to identify the **MOST CRUCIAL AND ESSENTIAL** SQL table names from the provided list that are absolutely necessary to answer the user's query.

**Consider a table essential if it:**
1.  Represents a primary entity or action directly mentioned (e.g., 'customers' for 'people', 'orders' for 'bought').
2.  Contains a column that is explicitly referenced for a **filtering condition** in the query (e.g., a 'brands' table if a specific brand name is mentioned, a 'stores' table if a specific store name or city is mentioned, or an 'orders' table if a specific year or date range is mentioned).
3.  Is directly involved in the core calculation or aggregation requested.

**Do NOT exclude tables just because they are "lookup" tables (like brands, categories, stores) if a specific value from them is used as a filter in the query.**

Given list of broadly relevant tables:
{broadly_relevant_tables}

User Query:
{user_query}

List **ONLY** the most crucial/essential table names (return only the table names as a list, e.g., ["customers", "orders", "brands"]):

"""

column_extraction_prompt = """

You are an expert SQL Analyst. Your task is to identify and return a list of column names and their data types that are strictly necessary to answer the given USER QUERY, **considering only the single database table described in the provided RELEVANT DOCUMENT.**

Follow these rules strictly:

1.  Your main goal is PRECISION — only extract column names and their data types that are directly required to compute or filter the final answer, **from the current table only.**

2. Providing a REASON for the column is MUST.

2.  You will receive:
    * A USER QUERY.
    * A single DOCUMENT describing **ONE** database TABLE and its columns (RELEVANT CHUNK).

3.  Based **ONLY** on this single document, extract **ONLY** those column names and their data types from **this current table** that contribute essential data toward answering the query.

4.  If the current table seems IRRELEVANT to the USER QUERY, or if NONE of its columns are necessary to filter, join, group, count, or compute the result from **this specific table** — RETURN an empty list `[]`.

5.  **CRUCIAL RULE FOR JOINING:** You MUST include **all Primary Key (PK)** columns and **Foreign Key (FK)** columns that are present in the provided table's schema document, **if this table is relevant to the query**. These keys are fundamental for joining tables correctly.

6.  Do NOT include other columns **from the current table** if they are:
    * Related to staff, store, shipping, or inventory **unless the query explicitly asks about these specific aspects of the current table's data.**
    * Describing taxonomy or grouping (like categories, subcategories, or tags) **unless the query directly asks for them or requires grouping by them from this table.**

7.  Examples of what **NOT** to include (unless directly and essentially required by the query from the current table):
    * If the query is about customers or product brands, and the current table is `staffs`, do not include `staff_id`, `manager_id`, etc., unless the query is *also* about staff.
    * If the query is about product sales, and the current table only includes category details (e.g., just `category_id`, `category_name`), and the query *doesn't* ask about categories, return `[]` or just the PK if it's a FK in another table.
    * If the query asks **how many people bought a brand of bike**, and the current table is `categories`, do **not** include category-related columns unless the query **explicitly** asks about the category.

8.  Strict Constraints on Output:
    * You must **ONLY** extract column names and their data types that exist **EXACTLY** as defined in the given `RELEVANT DOCUMENT`.
    * Do not invent or assume column names.
    * **IF** both `brand` and `category` information exist **in the current table**, and the query only mentions a brand (e.g., Electra), **prefer brand columns** and exclude category-related columns from **this table's output** unless explicitly required.
    * Do not infer additional tables — **stick strictly to the table described in the RELEVANT DOCUMENT.**
    * **Your output MUST be ONLY the list of tuples `[('column_name', 'data_type')]`. Do NOT include any additional text, explanations, or prose outside of this list.**

---

RELEVANT DOCUMENT:
{relevant_chunks}

USER QUERY:
{user_query}

If no columns are needed from this table, return: `[]`
"""

col_filter_prompt = """

USER QUERY:
{user_query}

1. You are an expert SQL Analyst. 
2. You are given a user query, and the columns, their data types and the reason of extraction. Very critically examine the reason, and decide if the reasoning is correct or not. You may also refer to the column name, as they explain the data they store. Referring to both of these, decide if the column is relevant or not.
3. These columns were initially found to be relevant for answering the user's query.
4. But some of the columns from the list of columns given to you *MIGHT ACTUALLY NOT* be relevant.
5. Your *JOB* is to understand the intent of the user's query, and filter out the columns which are not required.
6. You are supposed to be *EXTREMELY PRECISE*, and only list the necessary columns.
7. If you think a column is *RELEVANT*, return the column's name, its data type, and the *REASON*, why it was found to be relevant.

COLUMNS INITIALLY FOUND RELEVANT
{relevant_columns}

"""

query_generation_prompt = """
You are a professional SQL Analyst, working on a MySQL database named **bike_store**.
**IT IS VERY IMPORTANT THAT YOU ONLY USE FUNCTIONS USED IN MYSQL DATABASES.**

You are provided with:
- A natural language user query
- A list of relevant database tables
- A list of relationships (foreign key joins) between the tables
- A filtered list of relevant columns, with their data types and the reason why each was selected

Your task is to:

**NER(Named Entity Recognition) and Column Identification**
1. Carry out Named Entity Recognition to analyze the natural language user query to identify key entities such as categories, brands, dates, locations, specific metrics, and any other relevant keywords.
2. For each identified entity, map it to the most probable corresponding database column(s) based on common naming conventions and data types. This mapping is an internal step to guide your SQL generation.

**SQL Generation**
1. Understand the intent of the user's query. This is the most important part, as it defines ypur further steps.
2. Generate a syntactically correct SQL query that retrieves the correct answer.
3. Use **only the provided tables and columns**—do not introduce any extra columns or tables.
4. Some columns you are being provided, might not be relevant to the user query. You need to check each column name, and decide whether it is useful or not. The column_names are self-explanatory.
5. Use **only the relationships provided** to join the tables.
6. **Respect the column data types** when writing filters:
   - For example, if a date is stored as `text`, use string comparisons or cast if needed.
7. Ensure the SQL query applies all necessary filters, such as:
   - Category or brand filters (e.g., 'Electra' bikes)
   - Date-based filters (e.g., orders in 2023)
   - Location filters (e.g., store name = 'Santa Cruz')
8. If the query intent is to count people/customers, use `COUNT(DISTINCT ...)` appropriately.
9. Format your query cleanly and make it executable.

---

"""
