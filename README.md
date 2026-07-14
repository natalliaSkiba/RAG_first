# RAG_first

Python RAG project for searching French railway technical documents and generating educational quizzes for **aiguilleurs** and **agents de circulation (AC)**.

## Target Architecture

```text
Angular
→ Java Spring Boot
→ Python RAG API
→ Document retrieval
```

Java, Angular and the HTTP API are not implemented yet.

## Implemented

- PDF extraction and cleaning
- Document validation
- Section-based chunking
- Local embeddings
- Semantic search
- Hybrid search
- Retrieval evaluation
- Quiz context and prompt creation
- Quiz JSON parsing and source validation
- Local quiz generation with Ollama
- Quiz generation with Gemini
- Retry handling for temporary Gemini `429` and `503` errors
- Automated tests with `unittest`

## Embeddings

```text
Model: intfloat/multilingual-e5-small
Dimensions: 384
Chunks: approximately 455
```

## Project Structure

```text
data/                  Documents and generated data
src/chunking/          Document chunking
src/embedding/         Embedding generation
src/retrieval/         Semantic and hybrid search
src/quiz/              Quiz generation and validation
tests/                 Automated tests
main_*.py              Manual execution and diagnostic scripts
```

## Installation

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Main Commands

Generate chunks:

```powershell
python main_chunk.py
```

Generate embeddings:

```powershell
python main_generate_embeddings.py
```

Run hybrid search:

```powershell
python main_search_hybrid.py
```

Run retrieval evaluation:

```powershell
python main_evaluate_retrieval.py
```

Run all automated tests:

```powershell
python -m unittest discover -s tests -v
```

## Quiz Generation

The quiz is intended only for **aiguilleurs** and **agents de circulation**.

Questions must test their actions, decisions, checks, communications and responsibilities. Other railway roles may appear only as part of the situation.

### Ollama

```powershell
python main_test_ollama_quiz_generator.py
```

### Gemini

Set the API key for the current PowerShell session:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

Run the manual test:

```powershell
python main_test_gemini_quiz_generator.py
```

Do not store API keys in the source code or commit them to Git.

## Next Phase

Create a service around the existing hybrid search:

```text
application startup
→ load model once
→ load embeddings once
→ RetrievalService.search()
→ existing hybrid search
```

Next steps:

1. Create `RetrievalService`.
2. Add its automated test.
3. Add a FastAPI endpoint.
4. Connect Java Spring Boot.
5. Connect Angular.

The retrieval algorithm remains in Python.