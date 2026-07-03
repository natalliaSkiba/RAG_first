# RAG_first

An educational RAG (Retrieval-Augmented Generation) system for processing technical documentation, such as AMV railway manuals, and preparing it for semantic search and LLM-based question answering.

The project is written in Python and organized as a modular document-processing pipeline.

## Architecture

The project processes PDF documents through the following stages:

1. **Extraction** — converts PDF pages into Markdown using Docling and OCR.
2. **OCR Analysis** — analyzes extracted text, character frequency, word frequency, and suspicious OCR tokens.
3. **Cleaning** — removes technical artifacts and corrects confirmed OCR errors.
4. **Validation** — compares extracted and cleaned documents and checks that important Markdown structure has not been damaged.
5. **Chunking** — splits cleaned documents into smaller text chunks.
6. **Embeddings** — converts text chunks into vector representations.
7. **Vector Database** — stores embeddings for semantic search.
8. **RAG and LLM** — retrieves relevant context and generates answers.

## Current Status

### Implemented

- PDF extraction in small page batches
- Markdown generation with Docling and OCR
- Image extraction from PDF files
- OCR text analysis
- Character-frequency statistics
- Word-frequency statistics
- Detection of suspicious OCR tokens
- OCR text cleaning
- Replacement of tab characters with spaces
- Removal of `<!-- image -->` markers
- Removal of trailing spaces
- Normalization of excessive blank lines
- HTML entity decoding
- Correction of confirmed OCR errors through `OCR_REPLACEMENTS`
- Preservation of capitalization during OCR replacement
- Analysis of cleaned Markdown files
- Validation of:
  - Markdown filenames
  - missing or extra files
  - empty cleaned files
  - remaining tab characters
  - remaining image markers
  - Markdown heading markers
  - Markdown table markers

### Next Phase

- Text chunking of cleaned Markdown documents

### Planned

- Embedding generation
- Vector database integration
- Semantic search
- LLM-powered question answering

## Project Structure

```text
RAG_first/
│
├── data/
│   ├── raw/                         # Source PDF files
│   ├── extracted/                   # Raw Markdown files produced by OCR
│   ├── cleaned/                     # Cleaned Markdown files
│   ├── chunks/                      # Text chunks
│   ├── images/                      # Images extracted from PDF files
│   ├── reports/                     # OCR analysis reports
│   └── sample/                      # Small demonstration files committed to Git
│
├── src/
│   ├── __init__.py
│   │
│   ├── extraction/
│   │   ├── __init__.py
│   │   └── extract_pdf.py           # PDF extraction with Docling
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── analyze_ocr.py           # OCR statistics and error detection
│   │
│   ├── cleaning/
│   │   ├── __init__.py
│   │   ├── replacements.py          # Confirmed OCR replacements
│   │   └── rules.py                 # OCR cleaning rules
│   │
│   ├── validation/
│   │   ├── __init__.py
│   │   └── validate_cleaning.py     # Validation of cleaned documents
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
├── main_extract.py                  # Runs PDF extraction
├── main_analyze.py                  # Analyzes extracted Markdown files
├── main_clean.py                    # Cleans extracted Markdown files
├── main_analyze_clean.py            # Analyzes cleaned Markdown files
├── main_validate.py                 # Validates cleaning results
├── requirements.txt                 # Python dependencies
├── .gitignore
└── README.md
```

The `data/` directory contains local source documents and generated files.

Real documents, extracted images, OCR results, cleaned files, chunks, and reports are excluded from Git.

Only `.gitkeep` files and small demonstration files from `data/sample/` are committed.

## Extraction Strategy

Large PDF documents are processed in small page batches, for example five pages at a time.

This approach:

- reduces memory usage;
- makes processing more stable;
- allows extraction to resume after an interruption;
- produces smaller Markdown files that are easier to analyze, clean, and chunk.

Example output files:

```text
amv_001_005.md
amv_006_010.md
amv_011_015.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/natalliaSkiba/RAG_first.git
cd RAG_first
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

The project keeps the required empty data directories in Git through `.gitkeep` files.

Real source documents and generated outputs remain local and are ignored by Git.

## Sample Data

The repository contains small demonstration files that show the OCR cleaning result without including the complete source document.

```text
data/sample/sample_extracted.md
data/sample/sample_cleaned.md
```

`sample_extracted.md` contains a short fragment with typical OCR errors.

`sample_cleaned.md` contains the same fragment after applying the cleaning rules.

Example extracted text:

```text
Circula;on interdite.
Ar8cle 203.
Communica8on avec le conducteur.
```

Example cleaned text:

```text
Circulation interdite.
Article 203.
Communication avec le conducteur.
```

## Usage

The pipeline stages should be executed from the project root.

### 1. Run PDF extraction

```bash
python main_extract.py
```

Generated Markdown files are saved in:

```text
data/extracted/
```

Extracted images, when present, are saved in:

```text
data/images/
```

### 2. Analyze extracted OCR text

```bash
python main_analyze.py
```

The OCR analysis report is saved in:

```text
data/reports/ocr_analysis_report.md
```

The report contains:

- the number of extracted files;
- the total number of characters;
- the number of characters in each file;
- character-frequency statistics;
- word-frequency statistics;
- suspicious OCR tokens.

### 3. Clean extracted Markdown files

```bash
python main_clean.py
```

The cleaning stage reads files from:

```text
data/extracted/
```

and saves cleaned versions in:

```text
data/cleaned/
```

The cleaning stage currently:

- replaces tab characters with spaces;
- removes `<!-- image -->` markers;
- decodes HTML entities such as `&amp;`;
- normalizes excessive blank lines;
- removes trailing spaces;
- corrects confirmed OCR errors;
- preserves capitalization during replacements.

Examples:

```text
circula;on     → circulation
Ar8cle         → Article
Communica8on   → Communication
COMMUNICA8ON   → COMMUNICATION
```

Confirmed OCR replacements are stored in:

```text
src/cleaning/replacements.py
```

Cleaning rules are implemented in:

```text
src/cleaning/rules.py
```

### 4. Analyze cleaned Markdown files

```bash
python main_analyze_clean.py
```

The cleaned OCR analysis report is saved in:

```text
data/reports/ocr_analysis_cleaned_report.md
```

This report is used to:

- compare extracted and cleaned text;
- verify that frequent OCR errors were corrected;
- identify rare suspicious tokens that require manual review;
- avoid unsafe automatic replacements.

### 5. Validate cleaned Markdown files

```bash
python main_validate.py
```

The validation stage checks:

- that extracted and cleaned file counts are equal;
- that filenames are identical;
- that no cleaned file is empty;
- that tab characters were removed;
- that `<!-- image -->` markers were removed;
- that Markdown heading markers were preserved;
- that Markdown table markers were preserved.

A successful validation produces output similar to:

```text
Extracted files: 17
Cleaned files: 17
OK: filenames are identical
OK: no empty cleaned files
OK: no tab characters
OK: no image markers
OK: Markdown heading markers are preserved
OK: Markdown table markers are preserved
```

## OCR Cleaning Strategy

OCR corrections are applied conservatively.

The project does not replace every occurrence of characters such as `;` or `8`, because they may be valid punctuation marks, numbers, identifiers, or technical codes.

Instead, only confirmed incorrect words are added to `OCR_REPLACEMENTS`.

For example:

```python
OCR_REPLACEMENTS = {
    "circula;on": "circulation",
    "ar8cle": "article",
    "protec8on": "protection",
}
```

The cleaning process follows this cycle:

```text
analyze extracted text
        ↓
identify frequent OCR errors
        ↓
verify words in context
        ↓
add confirmed replacements
        ↓
clean all Markdown files
        ↓
analyze cleaned text
        ↓
validate the result
```

Rare or ambiguous OCR errors are intentionally left unchanged when their correct form cannot be determined safely from context.

## Technology Stack

- Python
- Docling
- OCR
- Regular expressions
- `pathlib`
- `collections.Counter`
- `html.unescape`

Additional technologies will be introduced during the next project phases.

## Next Development Phase

Phase 4 will implement chunking for files stored in:

```text
data/cleaned/
```

The chunking stage will prepare documents for:

```text
cleaned Markdown
        ↓
text chunks
        ↓
embeddings
        ↓
vector database
        ↓
semantic retrieval
        ↓
LLM-generated answers
```