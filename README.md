# NL-to-SQL

A sophisticated Retrieval-Augmented Generation (RAG) system that converts natural language queries into SQL queries for a bike store database. The system uses a multi-level approach with knowledge graphs and vector embeddings to intelligently identify relevant tables and columns.

## 🚀 Features

- **Multi-Level RAG Architecture**: Progressive refinement from broad table identification to specific column extraction
- **Knowledge Graph Integration**: Uses NetworkX to model database relationships and validate join paths
- **Vector Embeddings**: Leverages ChromaDB and OpenAI embeddings for semantic document retrieval
- **Intelligent Table Filtering**: Identifies seed tables and expands to connected tables using graph traversal
- **Column-Level Precision**: Extracts only relevant columns with reasoning for each selection
- **Multiple LLM Support**: Integrates OpenAI GPT-4o-mini, Groq Llama-3.3, and Qwen-QWQ models

## 🏗️ Architecture

### Level 1: Broad Table Identification
- Uses vector similarity search on database overview documentation
- Identifies potentially relevant tables with high recall
- Extracts seed tables that are most crucial for the query

### Level 2: Knowledge Graph Validation
- Validates table relationships using a pre-built knowledge graph
- Finds optimal join paths between seed tables
- Adds necessary intermediate tables for proper joins

### Level 3: Column Extraction
- Performs table-specific vector searches for detailed column information
- Uses structured output to extract relevant columns with data types and reasoning
- Applies filtering to ensure precision

### Level 4: SQL Generation
- Combines all gathered information to generate executable SQL queries
- Performs Named Entity Recognition (NER) for query understanding
- Generates MySQL-compatible queries with proper joins and filters

## 📁 Project Structure

```
├── RAG_pipeline.py           # Main pipeline orchestrator
├── model.py                  # Pydantic models and Knowledge Graph class
├── knowledge_graph.gml       # Pre-built database schema graph
├── requirements.txt          # Python dependencies
├── utilities/
│   ├── connect_mysql.py      # Database connection utilities
│   ├── prompts.py           # LLM prompts for each pipeline stage
│   ├── generate_KG.py       # Knowledge graph generation script
│   └── generate_embeddings/
│       ├── generate_db.py    # Vector store initialization
│       ├── retrieve_doc.py   # Document processing utilities
│       ├── gen_embed.py      # Overview embeddings generation
│       └── gen_table_embed.py # Table-specific embeddings generation
├── docs/
│   ├── overview.md          # Database overview documentation
│   └── table_docs/         # Individual table documentation
│       ├── brands.md
│       ├── categories.md
│       ├── customers.md
│       └── ... (other table docs)
└── db/                      # Vector database storage
    ├── overview_db/         # Overview embeddings
    └── table_db/           # Table-specific embeddings
```

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <your-repository-url>
cd rag-pipeline
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
```

4. **Configure database connection**
Update `utilities/connect_mysql.py` with your MySQL credentials:
```python
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="bike_store"
)
```

## 🚀 Usage

### Quick Start
```bash
python RAG_pipeline.py
```

The system will prompt you for a natural language query and then:
1. Identify relevant tables
2. Extract seed tables
3. Validate join paths using the knowledge graph
4. Extract relevant columns
5. Generate the final SQL query

### Example Queries
- "How many customers bought Electra bikes in 2023?"
- "What are the top 5 best-selling products by revenue?"
- "Which staff members processed the most orders last year?"
- "Show me the current inventory levels for mountain bikes at Santa Cruz store"

### Setting Up Embeddings

**Generate overview embeddings:**
```bash
cd utilities/generate_embeddings
python gen_embed.py
```

**Generate table-specific embeddings:**
```bash
python gen_table_embed.py
```

**Generate knowledge graph:**
```bash
cd utilities
python generate_KG.py
```

## 🗄️ Database Schema

The system works with a bike store sample database from Kaggle ([Bike Store Sample Database](https://www.kaggle.com/datasets/dillonmyrick/bike-store-sample-database)) containing these tables:
- **brands**: Product manufacturers
- **categories**: Product classifications
- **customers**: Customer information
- **orders**: Sales transactions
- **order_items**: Individual items within orders
- **products**: Product catalog
- **staffs**: Employee information
- **stocks**: Inventory levels by store
- **stores**: Store locations

## 🔧 Configuration

### Model Configuration
The pipeline uses different models for different stages:
- **OpenAI GPT-4o-mini**: Table and column extraction
- **Groq Llama-3.3-70b**: General reasoning tasks
- **Groq Qwen-QWQ-32b**: SQL query generation

### Vector Store Configuration
- **Embedding Model**: OpenAI text-embedding-3-large
- **Vector Database**: ChromaDB
- **Similarity Search**: Top-k retrieval with configurable k values

## 📊 Performance Optimization

- **Chunking Strategy**: Markdown header-based splitting for structured documents
- **Retrieval Parameters**: Tuned k values for different pipeline stages
- **Graph Algorithms**: Efficient shortest path finding for table relationships
- **Structured Output**: Pydantic models ensure consistent LLM responses

## 🧪 Extending the System

### Adding New Tables
1. Add table documentation to `docs/table_docs/`
2. Update the knowledge graph in `utilities/generate_KG.py`
3. Regenerate embeddings with `gen_table_embed.py`

### Custom Prompts
Modify prompts in `utilities/prompts.py` to adapt the system for different domains or query types.

### Additional Models
The system is designed to easily integrate new LLM providers through LangChain's unified interface.

## 🐛 Troubleshooting

### Common Issues
- **Empty results**: Check if embeddings are properly generated
- **Join path errors**: Verify knowledge graph relationships
- **SQL syntax errors**: Ensure table/column names match database schema

### Debugging
Enable verbose logging by adding print statements in the main pipeline for each stage's output.

## 📝 Dependencies

- `langchain_openai`: OpenAI model integration
- `langchain_groq`: Groq model integration
- `langchain_chroma`: Vector database
- `networkx`: Graph algorithms
- `pydantic`: Data validation
- `mysql-connector-python`: Database connectivity

## 📚 Dataset Attribution

This project uses the **Bike Store Sample Database** from Kaggle, created by Dillon Myrick:
- **Source**: [Bike Store Sample Database](https://www.kaggle.com/datasets/dillonmyrick/bike-store-sample-database)
- **License**: Please refer to the Kaggle dataset page for licensing information
- **Description**: A comprehensive sample database modeling a bike store's operations including products, customers, orders, inventory, and staff management

To use this project:
1. Download the database from the Kaggle link above
2. Import it into your MySQL instance
3. Update the connection parameters in `utilities/connect_mysql.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

For questions or issues, please open a GitHub issue or contact the development team.

---

**Note**: This system is designed for educational and research purposes. Ensure proper security measures when deploying in production environments.
