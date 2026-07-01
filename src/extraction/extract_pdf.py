from pathlib import Path
from pypdf import PdfReader
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions


def get_total_pages(pdf_path: str) -> int:
    """ Return total pages in PDF"""
    reader = PdfReader(pdf_path)
    return len(reader.pages)

def extract_pdf_in_batches(pdf_path: str, output_dir: str, batch_size: int, language=None):
    """Extract text and images from PDF in batches."""
    if language is None:
        language = ["fr"]
    base_dir = Path(output_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    image_dir = base_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)

    ## Pipeline options configuration
    pipeline_options = PdfPipelineOptions()
    pipeline_options.generate_picture_images = True

    ## Enable forced OCR and specify language(e.g., ["fr"])
    pipeline_options.do_ocr = True
    ocr_options = EasyOcrOptions(lang=language)
    pipeline_options.ocr_options = ocr_options

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    total_pages = get_total_pages(pdf_path)

    for start_page in range(1, total_pages + 1, batch_size):
        end_page = min(start_page + batch_size -1, total_pages)
        file_name = f"amv_{start_page:03d}_{end_page:03d}.md"
        output_path = base_dir / file_name

        if output_path.exists():
            print(f"*****Skipping {file_name} (useful for resuming work after a crash).*****")
            continue
        print(f"*****Processing page {start_page} to {end_page}*****")

        try:
            result = converter.convert(pdf_path, page_range=(start_page, end_page))

            md_content = result.document.export_to_markdown()

            ## Saving the text file to disk
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md_content)

            ##IMAGE EXTRACTING.
            pic_counter = 1
            for element, _ in result.document.iterate_items():

                ##Checking if the element is a picture.
                if type(element).__name__ == "PictureItem":

                    ## Extracting image bytes (in PIL Image format).
                    img_pil = element.get_image(result.document)

                    if img_pil:

                        ## Formatting the name for the image and saving it to the images' subfolder.
                        img_name = f"img_{start_page:03d}_{end_page:03d}_{pic_counter}.png"
                        img_pil.save(image_dir / img_name)
                        pic_counter += 1

            print(f"Saved: {file_name} (and {pic_counter - 1} images)")


        except Exception as e:
            print(f"Error processing page {start_page} to {end_page}: {e}")
