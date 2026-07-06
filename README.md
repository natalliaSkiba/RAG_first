# RAG_first

An educational RAG (Retrieval-Augmented Generation) system for processing technical documentation, such as AMV railway manuals, and preparing it for semantic search and LLM-based question answering.

The project is written in Python and organized as a modular document-processing pipeline.

## Architecture

The project processes PDF documents through the following stages:

1. **Extraction** — converts PDF pages into Markdown using Docling and OCR.
2. **OCR Analysis** — analyzes extracted text, character frequency, word frequency, and suspicious OCR tokens.
3. **Cleaning** — removes technical artifacts, corrects confirmed OCR errors, and preserves links to extracted images.
4. **Validation** — checks that the cleaning and chunking stages did not damage important document structure.
5. **Chunking** — splits cleaned Markdown documents into validated JSONL chunks with metadata.
6. **Embeddings** — converts chunks into vector representations.
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
- Conversion of `<!-- image -->` markers into explicit image paths
- Removal of trailing spaces
- Normalization of excessive blank lines
- HTML entity decoding
- Correction of confirmed OCR errors through `OCR_REPLACEMENTS`
- Preservation of capitalization during OCR replacement
- Analysis of cleaned Markdown files
- Validation of cleaned Markdown files
- Markdown heading preservation
- Markdown table preservation
- Markdown image marker parsing
- Section-based chunking
- Text splitting with overlap
- Preservation of complete Markdown tables as chunks
- Assignment of image metadata to chunks
- Chunk validation
- JSONL chunk writing
- Full chunking pipeline through `main_chunk.py`

### Current Chunking Result

The current AMV dataset produces:

```text
Documents: 17
Chunks: 455
Validation errors: 0
```

The chunking stage preserves:

- source filename;
- chunk number;
- heading;
- heading path;
- chunk type;
- linked images;
- section ID;
- source character positions.

### Next Phase

- Embedding generation from JSONL chunks

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
│   ├── chunks/                      # JSONL chunks generated from cleaned Markdown
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
│   │   ├── validate_cleaning.py     # Validation of cleaned documents
│   │   └── validate_chunking.py     # Validation of generated chunks
│   │
│   ├── chunking/
│   │   ├── __init__.py
│   │   ├── WORKFLOW.md              # Chunking workflow documentation
│   │   ├── models.py                # Data models for blocks, sections, chunks
│   │   ├── markdown_parser.py       # Markdown parser
│   │   ├── section_builder.py       # Section construction from parsed blocks
│   │   ├── chunker.py               # Section-to-chunk logic
│   │   └── writer.py                # JSONL writer
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
├── main_chunk.py                    # Generates validated JSONL chunks
├── requirements.txt                 # Python dependencies
├── .gitignore
└── README.md
```

The `data/` directory contains local source documents and generated files.

Real source documents and generated outputs may remain local depending on `.gitignore` rules and project needs.

Only files intentionally added to Git should be committed.

## Extraction Strategy

Large PDF documents are processed in small page batches, for example five pages at a time.

This approach:

- reduces memory usage;
- makes processing more stable;
- allows extraction to resume after an interruption;
- produces smaller Markdown files that are easier to analyze, clean, validate, and chunk.

Example output files:

```text
amv_001_005.md
amv_006_010.md
amv_011_015.md
```

Extracted images are saved separately in:

```text
data/images/
```

Example image files:

```text
img_001_005_1.png
img_011_015_1.png
img_011_015_2.png
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

Real source documents and generated outputs should be handled according to the repository `.gitignore` rules.

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
- converts `<!-- image -->` markers into explicit image-path markers;
- decodes HTML entities such as `&amp;`;
- normalizes excessive blank lines;
- removes trailing spaces;
- corrects confirmed OCR errors;
- preserves capitalization during replacements.

Example image marker before cleaning:

```markdown
<!-- image -->
```

Example image marker after cleaning:

```markdown
<!-- image: data/images/img_011_015_1.png -->
```

Examples of OCR corrections:

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
- that raw `<!-- image -->` markers were converted;
- that Markdown heading markers were preserved;
- that Markdown table markers were preserved.

A successful validation produces output similar to:

```text
Extracted files: 17
Cleaned files: 17
OK: filenames are identical
OK: no empty cleaned files
OK: no tab characters
OK: no raw image markers
OK: Markdown heading markers are preserved
OK: Markdown table markers are preserved
```

### 6. Generate JSONL chunks

```bash
python main_chunk.py
```

The chunking stage reads cleaned Markdown files from:

```text
data/cleaned/
```

and writes JSONL chunk files to:

```text
data/chunks/
```

A successful run produces output similar to:

```text
Chunked: amv_001_005.md -> amv_001_005.jsonl (28 chunks)
Chunked: amv_006_010.md -> amv_006_010.jsonl (43 chunks)
Chunked: amv_011_015.md -> amv_011_015.jsonl (27 chunks)

Chunking completed.
Documents: 17
Chunks: 455
```

Each JSONL line contains one chunk:

```json
{
  "id": "amv_011_015_chunk_0005",
  "text": "Chunk text...",
  "metadata": {
    "source": "amv_011_015.md",
    "chunk_number": 5,
    "heading": "amv_011_015",
    "heading_path": [],
    "chunk_type": "text",
    "images": [
      "data/images/img_011_015_1.png"
    ],
    "section_id": "section_001",
    "start_char": 0,
    "end_char": 5128,
    "size_chars": 986
  }
}
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

## Chunking Strategy

The chunking stage transforms cleaned Markdown into small validated chunks for later embedding generation.

The processing flow is:

```text
cleaned Markdown
        ↓
MarkdownBlock
        ↓
Section
        ↓
TextPart
        ↓
Chunk
        ↓
JSONL
```

### MarkdownBlock

A `MarkdownBlock` represents one structural block of a Markdown document.

Supported block types:

```text
heading
text
table
image
```

Image markers are parsed as image blocks and preserve the path to the extracted image.

### Section

A `Section` represents one educational topic or document section.

It groups related blocks together:

```text
Section
├── text block
├── image block
└── table block
```

### TextPart

A `TextPart` represents a smaller part of a section.

Long text sections are split into parts with overlap.

Images are assigned to the nearest relevant text part according to their position in the original Markdown document.

### Chunk

A `Chunk` is the final unit prepared for semantic search.

Each chunk contains:

- unique chunk ID;
- text;
- source metadata;
- heading metadata;
- chunk type;
- linked images.

## Chunking Rules

The current chunking rules are:

```text
MAX_CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150
```

Long text is split using natural boundaries when possible:

1. paragraph break;
2. sentence boundary;
3. whitespace.

Markdown tables are preserved as complete chunks, even when they are longer than `MAX_CHUNK_SIZE`.

This avoids breaking table structure.

Sections containing only images are preserved by using the section heading as searchable text and storing the image path in chunk metadata.

## Image Handling

Images are extracted from PDF files into:

```text
data/images/
```

During cleaning, raw image markers are converted from:

```markdown
<!-- image -->
```

to:

```markdown
<!-- image: data/images/img_011_015_1.png -->
```

During parsing, these markers become `image` blocks.

During chunking, image paths are stored in:

```python
chunk.metadata.images
```

This allows later RAG answers to include related diagrams or visual references together with retrieved text.

## Validation Strategy

The project contains validation for both cleaned Markdown and generated chunks.

Cleaning validation is implemented in:

```text
src/validation/validate_cleaning.py
```

Chunking validation is implemented in:

```text
src/validation/validate_chunking.py
```

Chunk validation checks:

- non-empty chunk ID;
- non-empty chunk text;
- valid source filename;
- valid chunk number;
- non-empty heading;
- maximum text size for non-table chunks;
- existing linked image files;
- duplicate chunk IDs;
- sequential chunk numbering.

The current AMV dataset passes chunking validation with:

```text
Documents: 17
Chunks: 455
Errors: 0
```

## JSONL Output

The chunking stage writes one JSONL file per cleaned Markdown document.

Example:

```text
data/chunks/amv_001_005.jsonl
data/chunks/amv_006_010.jsonl
data/chunks/amv_011_015.jsonl
```

Each line is a complete JSON object representing one chunk.

This format is suitable for:

- embedding generation;
- batch processing;
- indexing in a vector database;
- later retrieval in a RAG pipeline.

## Manual Test Scripts

During development, manual test scripts may be used to verify individual pipeline steps.

Examples:

```text
test_validate_chunking.py
test_validate_all_chunking.py
test_writer.py
test_all_chunks.py
```

These scripts are useful for development checks but are not part of the final application pipeline.

The main production entry point for chunk generation is:

```text
main_chunk.py
```

## Technology Stack

- Python
- Docling
- OCR
- Regular expressions
- JSONL
- `pathlib`
- `dataclasses`
- `collections.Counter`
- `html.unescape`

Additional technologies will be introduced during the next project phases.

## Next Development Phase

The next phase will generate embeddings for files stored in:

```text
data/chunks/
```

The next processing flow will be:

```text
JSONL chunks
        ↓
embeddings
        ↓
vector database
        ↓
semantic retrieval
        ↓
LLM-generated answers
```

The embedding stage will prepare chunks for semantic search and future RAG-based question answering.