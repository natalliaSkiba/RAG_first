import sys
from pathlib import Path  # <-- Этот импорт решает ошибку со скриншота
from src.extraction.extract_pdf import extract_pdf_in_batches

if __name__ == "__main__":
    pdf_document = "data/raw/AMV COMPLET.pdf"
    output_directory = "data/extracted"

    # SOURCE FILE EXISTENCE CHECK
    if not Path(pdf_document).is_file():
        print(f"Error: PDF file not found at '{pdf_document}'.")
        print("Please check the path and try again.")
        sys.exit(1)

    print("Starting Phase 1: Extraction")

    extract_pdf_in_batches(
        pdf_path=pdf_document,
        output_dir=output_directory,
        batch_size=5,
        language=["fr"]
    )

    print("Phase 1 completed.")