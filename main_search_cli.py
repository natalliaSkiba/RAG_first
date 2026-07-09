import argparse
from pathlib import Path

from src.embedding.config import DEFAULT_EMBEDDING_CONFIG
from src.embedding.local_provider import LocalSentenceTransformerProvider
from src.retrieval.query import generate_query_embedding
from src.retrieval.reader import read_embedding_records_from_folder
from src.retrieval.search import search_by_vector_hybrid


def parse_arguments() -> argparse.Namespace:
    """Parses command line arguments."""

    parser = argparse.ArgumentParser(
        description="Run local hybrid semantic search over AMV embeddings.",
    )

    parser.add_argument(
        "question",
        type=str,
        help="User question for retrieval search.",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of search results to return.",
    )

    parser.add_argument(
        "--input-folder",
        type=Path,
        default=Path("data/embeddings"),
        help="Folder with embedding JSONL files.",
    )

    return parser.parse_args()


def main() -> None:
    """ Runs hybrid semantic search from command line."""

    args = parse_arguments()

    question = args.question.strip()

    if not question:
        raise ValueError("Question must not be empty")

    config = DEFAULT_EMBEDDING_CONFIG

    print("Hybrid semantic search CLI")
    print(f"Question: {question}")
    print(f"Input folder: {args.input_folder}")
    print(f"Model: {config.model_name}")
    print(f"Top-k: {args.top_k}")
    print()

    records = read_embedding_records_from_folder(
        input_folder=args.input_folder,
    )

    provider = LocalSentenceTransformerProvider(
        config=config,
    )

    query_embedding = generate_query_embedding(
        question=question,
        provider=provider,
    )

    results = search_by_vector_hybrid(
        question=question,
        query_embedding=query_embedding,
        records=records,
        top_k=args.top_k,
    )

    print(f"Loaded records: {len(records)}")
    print(f"Query embedding dimension: {len(query_embedding)}")
    print()

    print("Top results:")
    print("=" * 80)

    for result in results:
        record = result.record
        metadata = record.metadata

        text_preview = record.text.replace("\n", " ")
        text_preview = text_preview[:700]

        print(f"Rank: {result.rank}")
        print(f"Final score: {result.score:.6f}")
        print(f"Semantic score: {result.semantic_score:.6f}")
        print(f"Keyword score: {result.keyword_score:.6f}")
        print(f"ID: {record.chunk_id}")
        print(f"Source: {metadata.get('source')}")
        print(f"Heading: {metadata.get('heading')}")
        print(f"Chunk type: {metadata.get('chunk_type')}")
        print(f"Images: {record.get_images()}")
        print()
        print("Text preview:")
        print(text_preview)
        print("-" * 80)

    print()
    print("Hybrid semantic search CLI completed.")


if __name__ == "__main__":
    main()