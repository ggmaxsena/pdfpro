from io import BytesIO
import zipfile
from typing import Tuple

import pikepdf
from PyPDF2 import PdfReader, PdfWriter


class PDFService:
    """Regras de negócio para compressão e divisão de PDFs."""

    @staticmethod
    def compress(file_obj) -> Tuple[str, BytesIO]:
        pdf = pikepdf.open(file_obj)
        output = BytesIO()
        pdf.save(
            output,
            compress_streams=True,
            linearize=True,
            recompress_flate=True,
        )
        output.seek(0)
        return f"compressed_{file_obj.name}", output

    @staticmethod
    def split_by_pages(file_obj, start: int, end: int) -> Tuple[str, BytesIO]:
        reader = PdfReader(file_obj)
        writer = PdfWriter()

        for i in range(start - 1, end):
            writer.add_page(reader.pages[i])

        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return f"split_{file_obj.name}", output

    @staticmethod
    def split_by_size(file_obj, max_size_mb: int) -> Tuple[str, BytesIO]:
        max_bytes = max_size_mb * 1024 * 1024
        reader = PdfReader(file_obj)
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zf:
            part = 1
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

                tmp = BytesIO()
                writer.write(tmp)
                if tmp.tell() > max_bytes:         # estourou tamanho
                    # retrocede uma página
                    writer.pages.pop()
                    part_buf = BytesIO()
                    writer.write(part_buf)
                    part_buf.seek(0)
                    zf.writestr(f"part_{part}.pdf", part_buf.read())

                    writer = PdfWriter()
                    writer.add_page(page)
                    part += 1

            if len(writer.pages):
                part_buf = BytesIO()
                writer.write(part_buf)
                part_buf.seek(0)
                zf.writestr(f"part_{part}.pdf", part_buf.read())

        zip_buffer.seek(0)
        return f"split_by_size_{file_obj.name}.zip", zip_buffer