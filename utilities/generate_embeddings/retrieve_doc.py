from langchain_text_splitters import MarkdownHeaderTextSplitter

def get_doc_content(file_path:str) -> str:
    """Read the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_chunks(doc_content: str) -> list:
    """Split the document content into chunks based on headers."""
    # This will create a separate chunk for each '### a. brands', '### b. categories', etc.
    # The 'Header 2' split ensures "Table Summaries" itself is a chunk, and then its sub-sections.
    headers_to_split_on = [
        ("##", "Header 2"), # For sections like "Table Summaries", "Real-world Entity Relationships"
        ("###", "Header 3")  # Crucially, for individual table descriptions (a. brands, b. categories, etc.)
    ]
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
    )
    return splitter.split_text(doc_content)