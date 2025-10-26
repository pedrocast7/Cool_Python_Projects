import pypdf
import sys

path_to_watermark_file = sys.argv[1]
path_to_pdf_to_watermark = sys.argv[2]

with open(path_to_pdf_to_watermark, 'rb') as pdf_to_watermark:
    reader = pypdf.PdfReader(pdf_to_watermark)
    writer = pypdf.PdfWriter()
    for page_num in range(reader.get_num_pages()):
        page = reader.get_page(page_num)
        page.merge_page(pypdf.PdfReader(path_to_watermark_file).get_page(0))
        # Write the result back
        writer.add_page(page)

    with open("watermarked_document.pdf", "wb") as output:
        writer.write(output)
