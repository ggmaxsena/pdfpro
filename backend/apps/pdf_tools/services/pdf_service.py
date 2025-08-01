from io import BytesIO
from pathlib import Path
from typing import List, Tuple
import zipfile

import pikepdf


class PDFService:
    """
    Serviços de manipulação de PDF.
    """

    @staticmethod
    def _write_pdf(writer: pikepdf.Pdf, name: str) -> Tuple[str, BytesIO]:
        """
        Gera um buffer em memória com o conteúdo do `writer`.
        """
        buf = BytesIO()
        writer.save(buf)
        buf.seek(0)
        return name, buf

    @classmethod
    def compress(cls, file_obj) -> Tuple[str, BytesIO]:
        """
        Comprime um PDF.

        Args:
            file_obj: O objeto de arquivo do PDF a ser comprimido.

        Returns:
            Uma tupla contendo o nome do arquivo comprimido e um BytesIO
            com o conteúdo do PDF comprimido.
        """
        original_name = Path(file_obj.name).stem
        reader = pikepdf.Pdf.open(file_obj)
        writer = pikepdf.Pdf.new()

        for page in reader.pages:
            writer.pages.append(page)

        # Exemplo de compressão: remover objetos não utilizados
        # writer.remove_unreferenced_objects()

        compressed_name = f"compressed_{original_name}.pdf"
        return cls._write_pdf(writer, compressed_name)

    @classmethod
    def split_by_pages(cls, file_obj, start_page: int, end_page: int) -> Tuple[str, BytesIO]:
        """
        Divide um PDF por intervalo de páginas.

        Args:
            file_obj: O objeto de arquivo do PDF a ser dividido.
            start_page: A página inicial (base 1) para a divisão.
            end_page: A página final (base 1) para a divisão.

        Returns:
            Uma tupla contendo o nome do arquivo dividido e um BytesIO
            com o conteúdo do PDF dividido.
        """
        original_name = Path(file_obj.name).stem
        reader = pikepdf.Pdf.open(file_obj)
        writer = pikepdf.Pdf.new()

        # Ajusta para índice base 0
        start_idx = max(0, start_page - 1)
        end_idx = min(len(reader.pages), end_page)

        for i in range(start_idx, end_idx):
            writer.pages.append(reader.pages[i])

        split_name = f"split_{original_name}_pages_{start_page}-{end_page}.pdf"
        return cls._write_pdf(writer, split_name)

    @classmethod
    def split_by_size(cls, file_obj, size_mb: int) -> Tuple[str, BytesIO]:
        """
        Divide `file_obj` em múltiplos PDFs, cada um com tamanho
        aproximado menor ou igual a `size_mb`.  
        Retorna um ZIP contendo todas as partes.

        Estratégia:
        1. Abre o PDF original com pikepdf.
        2. Cria um novo PdfWriter e adiciona páginas até
           atingir o limite (`size_limit`).
        3. Quando exceder, remove a última página, salva o
           trecho e inicia um novo writer.
        4. Após processar todas as páginas, comprime tudo em ZIP.
        """
        size_limit = size_mb * 1024 * 1024
        original_name = Path(file_obj.name).stem
        reader = pikepdf.Pdf.open(file_obj)

        parts: List[Tuple[str, BytesIO]] = []
        writer = pikepdf.Pdf.new()
        part_idx = 1

        for i, page in enumerate(reader.pages, start=1):
            writer.pages.append(page)
            # Testa tamanho parcial
            tmp_name, tmp_buf = cls._write_pdf(writer, f"{original_name}_part{part_idx}.pdf")
            if tmp_buf.getbuffer().nbytes > size_limit:
                # Salva parte válida (sem a última página que estourou o limite)
                # Cria um novo writer com as páginas anteriores
                valid_writer = pikepdf.Pdf.new()
                for p in writer.pages[:-1]:
                    valid_writer.pages.append(p)
                
                tmp_name, tmp_buf = cls._write_pdf(valid_writer, f"{original_name}_part{part_idx}.pdf")
                parts.append((tmp_name, tmp_buf))

                # Reinicia writer com a página que ficou de fora
                part_idx += 1
                writer = pikepdf.Pdf.new()
                writer.pages.append(page)

        # Salva último fragmento
        if writer.pages:
            tmp_name, tmp_buf = cls._write_pdf(writer, f"{original_name}_part{part_idx}.pdf")
            parts.append((tmp_name, tmp_buf))

        # Compacta todas as partes em ZIP
        zip_buf = BytesIO()
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for fname, buf in parts:
                zf.writestr(fname, buf.getvalue())
        zip_buf.seek(0)

        zip_name = f"split_{original_name}.zip"
        return zip_name, zip_buf