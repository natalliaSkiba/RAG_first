# Antoni RAG Project

An educational RAG (Retrieval-Augmented Generation) system designed to process technical documentation (e.g., AMV manuals) and provide an LLM-powered interface for interactive learning. 

This project is built using Python and is structured as a modular data processing pipeline.

## 🏗 Architecture (The Data Pipeline)

The project follows a strict separation of concerns, processing raw PDF data through a 7-step pipeline to eventually feed a Large Language Model (LLM).

1. **Extraction** (Implemented) - Converts raw PDFs into raw Markdown and extracts images using `docling` and OCR.
2. **Cleaning** (Planned) - Removes OCR artifacts and irrelevant characters.
3. **Normalization** (Planned) - Standardizes the text format.
4. **Chunking** (Planned) - Splits the text into semantically meaningful overlapping chunks.
5. **Embeddings** (Planned) - Converts text chunks into vector representations.
6. **Vector DB** (Planned) - Stores vectors for semantic search (e.g., ChromaDB).
7. **RAG & LLM** (Planned) - Retrieves relevant context and generates answers.

## 📂 Project Structure

```text
antoni_rag_project/
│
├── data/                       # Data directory (ignored in Git)
│   ├── 01_raw/                 # Source PDF files (e.g., AMV COMPLET.pdf)
│   ├── 02_extracted/           # Phase 1 output (.md files and /images)
│   ├── 03_cleaned/             # Phase 2 output
│   └── 04_chunks/              # Phase 4 output
│
├── src/                        # Source code for the pipeline
│   ├── __init__.py             
│   ├── extract.py              # Phase 1: Batch extraction logic using Docling
│   └── ...                     # Future modules (clean.py, chunk.py, etc.)
│
├── vector_store/               # Vector database storage
├── main.py                     # Entry point to run the pipeline
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys)
└── .gitignore

🚀 Current State: Phase 1 (Extraction)
The current implementation focuses entirely on Phase 1: Extraction.

Tool: Uses IBM's docling library with EasyOCR.

Strategy: Processes PDFs in smaller batches (e.g., 5 pages at a time) to optimize RAM usage and allow the pipeline to resume safely in case of a crash.

Output: Generates raw .md files containing text and automatically formatted markdown tables, alongside a subfolder of extracted .png images.

⚙️ Installation & Setup
Clone the repository:

Bash
git clone <repository_url>
cd antoni_rag_project
Create and activate a virtual environment:

Bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
Install dependencies:
Make sure you are using the latest version of docling to ensure pipeline compatibility.

Bash
pip install --no-cache-dir -r requirements.txt
Prepare the data:
Place your source PDF file (e.g., AMV COMPLET.pdf) into the data/01_raw/ directory.

▶️ Usage
To execute the data pipeline, run the main script from the root directory:

Bash
python main.py