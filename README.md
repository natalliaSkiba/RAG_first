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
- Semantic and hybrid search
- Retrieval evaluation
- Reusable `RetrievalService`
- Quiz context and prompt creation
- Quiz JSON parsing and source validation
- Quiz generation with Ollama and Gemini
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

```powershell
python main_chunk.py
python main_generate_embeddings.py
python main_search_hybrid.py
python main_evaluate_retrieval.py
```

Run all automated tests:

```powershell
python -m unittest discover -s tests -v
```

## Quiz Generation

The quiz is intended only for **aiguilleurs** and **agents de circulation**.

Questions must test their actions, decisions, checks, communications and responsibilities. Other railway roles may appear only as part of the situation.

Run Ollama:

```powershell
python main_test_ollama_quiz_generator.py
```

Run Gemini:

```powershell
$env:GEMINI_API_KEY="your-api-key"
python main_test_gemini_quiz_generator.py
```

Do not store API keys in source code or commit them to Git.

## Retrieval Service

`RetrievalService` provides a reusable interface around the existing hybrid search.

```text
prepared embedding provider
+ loaded embedding records
→ RetrievalService.search(question, top_k)
→ query embedding
→ existing hybrid search
→ ranked chunks
```

The service receives an already prepared embedding provider and loaded embedding records. It does not reload them for every search request.

Example:

```python
service = RetrievalService(
    provider=provider,
    records=records,
)

results = service.search(
    question="Que faire en cas de détresse ?",
    top_k=5,
)
```

## Tests

```text
Ran 17 tests
OK
```

## Next Phase

Expose the retrieval service through a Python HTTP API:

```text
POST /api/v1/search
→ RetrievalService
→ hybrid search
→ JSON response
```

Next steps:

1. Create the FastAPI application.
2. Add the search endpoint.
3. Add an endpoint integration test.
4. Verify the API through Swagger.
5. Connect Java Spring Boot.
6. Connect Angular.