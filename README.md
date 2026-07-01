# Antoni RAG Project

An educational RAG (Retrieval-Augmented Generation) system for processing technical documentation, such as AMV railway manuals, and preparing it for semantic search and LLM-based question answering.

The project is written in Python and organized as a modular data-processing pipeline.

## Architecture

The project processes PDF documents through the following stages:

1. **Extraction** — converts PDF pages into Markdown using Docling and OCR.
2. **OCR Analysis** — analyzes extracted text, character frequency, word frequency, and suspicious OCR tokens.
3. **Cleaning** — removes OCR artifacts and irrelevant content.
4. **Validation** — compares raw and cleaned documents and checks that important information has not been lost.
5. **Chunking** — splits documents into smaller overlapping text chunks.
6. **Embeddings** — converts text chunks into vector representations.
7. **Vector Database** — stores embeddings for semantic search.
8. **RAG and LLM** — retrieves relevant context and generates answers.

## Current Status

### Implemented

- PDF extraction in small page batches
- Markdown generation
- OCR text analysis
- Character-frequency statistics
- Word-frequency statistics
- Detection of suspicious OCR tokens such as:
  - `circula;on`
  - `protec;on`
  - `ar8cle`
  - `installa8ons`
- Markdown analysis report generation

### In Progress

- OCR cleaning rules
- Cleaning validation

### Planned

- Text chunking
- Embedding generation
- Vector database integration
- Semantic search
- LLM-powered question answering

## Project Structure

```text
antoni_rag_project/
│
├── data/
│   ├── raw/                     # Source PDF files
│   ├── extracted/               # Raw Markdown files produced by OCR
│   ├── cleaned/                 # Cleaned Markdown files
│   ├── chunks/                  # Text chunks
│   └── reports/                 # OCR analysis and validation reports
│
├── src/
│   ├── __init__.py
│   │
│   ├── extraction/
│   │   ├── __init__.py
│   │   └── extract_pdf.py       # PDF extraction with Docling
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── analyze_ocr.py       # OCR statistics and error detection
│   │
│   ├── cleaning/
│   │   ├── __init__.py
│   │   └── rules.py             # OCR cleaning rules
│   │
│   ├── validation/
│   │   └── __init__.py
│   │
│   ├── chunking/
│   │   └── __init__.py
│   │
│   ├── embedding/
│   │   └── __init__.py
│   │
│   ├── vectordb/
│   │   └── __init__.py
│   │
│   └── rag/
│       └── __init__.py
│
├── main_extract.py              # Runs PDF extraction
├── main_analyze.py              # Runs OCR analysis
├── requirements.txt             # Python dependencies
├── .gitignore
└── README.md
```

The `data/` directory contains source documents and generated files and should not be committed to Git.

## Extraction Strategy

Large PDF documents are processed in small batches, for example five pages at a time.

This approach:

- reduces memory usage;
- makes processing more stable;
- allows extraction to resume after an interruption;
- produces smaller Markdown files that are easier to analyze and clean.

Example output files:

```text
amv_001_005.md
amv_006_010.md
amv_011_015.md
```

## Installation

Clone the repository:

```bash
git clone <repository_url>
cd antoni_rag_project
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install --no-cache-dir -r requirements.txt
```

## Data Preparation

Place the source PDF in:

```text
data/raw/
```

Example:

```text
data/raw/AMV COMPLET.pdf
```

## Usage

### Run PDF extraction

```bash
python main_extract.py
```

The generated Markdown files are saved in:

```text
data/extracted/
```

### Run OCR analysis

```bash
python main_analyze.py
```

The analysis report is saved in:

```text
data/reports/ocr_analysis_report.md
```

## OCR Analysis

The analysis stage currently collects:

- the number of extracted files;
- the total number of characters;
- the number of characters in each file;
- character-frequency statistics;
- word-frequency statistics;
- frequently occurring suspicious OCR tokens.

The report is used to identify systematic OCR errors before cleaning rules are applied.

## Technology Stack

- Python
- Docling
- OCR
- Regular expressions
- `pathlib`
- `collections.Counter`

Additional technologies will be introduced during the next project phases.