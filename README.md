# RAG_first

Educational RAG project for processing AMV railway manuals and preparing them for semantic search and future LLM-based question answering.

The project is written in Python and built as a modular document-processing pipeline.

## Current Status

Implemented:

* PDF extraction with Docling and OCR
* OCR analysis and cleaning
* Markdown validation
* Section-based chunking
* JSONL chunk generation
* Local embedding generation with `intfloat/multilingual-e5-small`
* Embedding validation
* Local semantic search over generated embeddings
* Hybrid search: semantic similarity + keyword boost
* Retrieval evaluation with test questions and metrics

Current AMV dataset:

```text
Documents: 17
Chunks: 455
Embedding records: 455
Embedding dimension: 384
Validation errors: 0
```

Current retrieval evaluation:

```text
Questions: 16

Semantic search:
Hit@1: 87.50%
Hit@5: 93.75%
MRR@5: 90.62%
Recall@5: 91.67%

Hybrid search:
Hit@1: 100.00%
Hit@5: 100.00%
MRR@5: 100.00%
Recall@5: 97.92%
```

Hybrid search currently performs better than pure semantic search on the evaluation set.

## Pipeline

```text
PDF
 ↓
OCR Markdown
 ↓
Cleaned Markdown
 ↓
Validated chunks
 ↓
Embeddings
 ↓
Semantic / hybrid retrieval
 ↓
Future: vector database
 ↓
Future: LLM answers
```

## Project Structure

```text
RAG_first/
│
├── data/
│   ├── raw/                 # Source PDF files
│   ├── extracted/           # OCR Markdown files
│   ├── cleaned/             # Cleaned Markdown files
│   ├── chunks/              # JSONL chunks
│   ├── embeddings/          # Generated embedding JSONL files
│   ├── evaluation/          # Retrieval test cases and candidates
│   ├── images/              # Extracted PDF images
│   ├── reports/             # OCR reports
│   └── sample/              # Small sample files committed to Git
│
├── src/
│   ├── extraction/          # PDF extraction
│   ├── analysis/            # OCR analysis
│   ├── cleaning/            # OCR cleaning rules
│   ├── validation/          # Cleaning, chunking, embedding validation
│   ├── chunking/            # Markdown parsing and chunk generation
│   ├── embedding/           # Embedding generation
│   ├── retrieval/           # Semantic and hybrid search
│   ├── vectordb/            # Future vector database integration
│   └── rag/                 # Future LLM-based RAG logic
│
├── main_extract.py
├── main_analyze.py
├── main_clean.py
├── main_analyze_clean.py
├── main_validate.py
├── main_chunk.py
├── main_generate_embeddings.py
├── main_validate_embeddings.py
├── main_search.py
├── main_search_hybrid.py
├── main_evaluate_retrieval.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/natalliaSkiba/RAG_first.git
cd RAG_first
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install --no-cache-dir -r requirements.txt
```

## Data Preparation

Place source PDF files in:

```text
data/raw/
```

Example:

```text
data/raw/AMV COMPLET.pdf
```

Generated files may remain local depending on `.gitignore`.

Usually local only:

```text
data/extracted/
data/cleaned/
data/chunks/
data/embeddings/
data/images/
data/reports/
```

Small sample files can be committed in:

```text
data/sample/
```

## Usage

Run all commands from the project root.

### 1. Extract PDF to Markdown

```bash
python main_extract.py
```

Output:

```text
data/extracted/
data/images/
```

### 2. Analyze OCR output

```bash
python main_analyze.py
```

Output:

```text
data/reports/ocr_analysis_report.md
```

### 3. Clean OCR Markdown

```bash
python main_clean.py
```

Input:

```text
data/extracted/
```

Output:

```text
data/cleaned/
```

Cleaning includes:

* removing technical artifacts
* converting image markers
* decoding HTML entities
* normalizing blank lines
* correcting confirmed OCR errors

Confirmed OCR replacements are stored in:

```text
src/cleaning/replacements.py
```

### 4. Analyze cleaned Markdown

```bash
python main_analyze_clean.py
```

Output:

```text
data/reports/ocr_analysis_cleaned_report.md
```

### 5. Validate cleaned Markdown

```bash
python main_validate.py
```

Validation checks:

* matching filenames
* non-empty files
* no tab characters
* converted image markers
* preserved Markdown headings
* preserved Markdown tables

### 6. Generate chunks

```bash
python main_chunk.py
```

Input:

```text
data/cleaned/
```

Output:

```text
data/chunks/
```

Current result:

```text
Documents: 17
Chunks: 455
Validation errors: 0
```

### 7. Generate embeddings

Test the local embedding provider:

```bash
python main_test_local_embedding_provider.py
```

Generate real embeddings:

```bash
python main_generate_embeddings.py
```

Validate embeddings:

```bash
python main_validate_embeddings.py
```

Current embedding configuration:

```text
Provider: local
Model: intfloat/multilingual-e5-small
Dimension: 384
Passage prefix: passage:
Query prefix: query:
Normalize embeddings: True
Batch size: 32
```

Output:

```text
data/embeddings/
```

### 8. Run semantic search

```bash
python main_search.py
```

This searches by vector similarity only.

### 9. Run hybrid search

```bash
python main_search_hybrid.py
```

Hybrid search combines:

```text
semantic score + keyword score
```

This improves retrieval for technical terms such as:

```text
DÉTRESSE
DSEC
secours
refoulez
```

### 10. Evaluate retrieval quality

Check test cases:

```bash
python main_check_retrieval_test_cases.py
```

Run evaluation:

```bash
python main_evaluate_retrieval.py
```

Evaluation file:

```text
data/evaluation/retrieval_test_cases.json
```

Candidate chunks file:

```text
data/evaluation/retrieval_candidates.md
```

Current evaluation result:

```text
Hybrid search:
Success: 16/16
Hit@1: 100.00%
Hit@5: 100.00%
MRR@5: 100.00%
Recall@5: 97.92%
```

## OCR Cleaning Strategy

OCR correction is conservative.

The project does not blindly replace every suspicious character such as `8` or `;`.

Only confirmed OCR errors are added to:

```text
src/cleaning/replacements.py
```

Example:

```python
OCR_REPLACEMENTS = {
    "circula;on": "circulation",
    "ar8cle": "article",
    "communica8on": "communication",
}
```

Cleaning cycle:

```text
analyze
 ↓
identify OCR errors
 ↓
confirm in context
 ↓
add safe replacements
 ↓
clean
 ↓
validate
```

Ambiguous OCR errors are left unchanged until they can be safely confirmed.

## Chunking Strategy

Cleaned Markdown is transformed into small searchable chunks.

Chunking preserves:

* source filename
* chunk ID
* heading
* heading path
* chunk type
* linked images
* source positions

Current rules:

```text
MAX_CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150
```

Long text is split using natural boundaries when possible:

1. paragraph break
2. sentence boundary
3. whitespace

Markdown tables are preserved as complete chunks.

Images are stored in metadata and remain available for future RAG answers.

## Embedding Strategy

The current baseline model is:

```text
intfloat/multilingual-e5-small
```

The project follows the E5 prefix convention:

```text
passage: <chunk text>
query: <user question>
```

Chunk embeddings include heading + text, because technical manuals often store the main topic in the heading.

Embedding records preserve:

* chunk ID
* chunk text
* chunk metadata
* image metadata
* embedding vector
* model metadata
* vector dimension
* normalization setting

## Retrieval Strategy

The project currently supports two retrieval modes.

### Semantic search

Uses vector similarity only.

Good for general meaning, but can miss technical terms.

### Hybrid search

Uses:

```text
final_score = semantic_score + keyword_score
```

This improves retrieval for domain-specific terms.

Keyword scoring includes:

* accent normalization
* `œ → oe` normalization
* French stopword filtering
* domain-specific query expansion
* filtering of overly generic domain terms

Example domain expansions:

```text
detresse → detresse, dsec, secours, degagement
secours  → secours, dsec, detresse, degagement
```

## Validation Strategy

The project validates each major pipeline stage.

Validation modules:

```text
src/validation/validate_cleaning.py
src/validation/validate_chunking.py
src/validation/validate_embeddings.py
```

Retrieval quality is evaluated with:

```text
src/retrieval/evaluation.py
```

Current retrieval metrics:

* Hit@1
* Hit@5
* MRR@5
* Recall@5

## Technology Stack

* Python
* Docling
* OCR
* Markdown
* JSONL
* pathlib
* dataclasses
* regular expressions
* sentence-transformers
* Hugging Face model hub
* intfloat/multilingual-e5-small
* vector embeddings

## Next Steps

Planned next phases:

1. Expand retrieval evaluation from 16 to 30+ questions.
2. Add more domain-specific query expansions.
3. Compare current model with alternatives such as `BAAI/bge-m3`.
4. Integrate a vector database.
5. Add context selection for future LLM answers.
6. Add LLM-based answer generation only after retrieval quality is stable.
