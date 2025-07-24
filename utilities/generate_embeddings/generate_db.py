from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def get_vector_store(name:str, db_path: str) -> Chroma:
    """Get the vector store instance."""
    
    embeddings = OpenAIEmbeddings(model = "text-embedding-3-large")

    vector_store = Chroma(
        collection_name=name,
        persist_directory=db_path,
        embedding_function = embeddings,
    )
    return vector_store






