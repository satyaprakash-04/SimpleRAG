from ETL.extract.base import BaseFileReader
import pymupdf
from typing import Any


class PDFReader(BaseFileReader):

    def read(self, path) -> dict[str, Any]:
        data_dict = {}
        pdf_text = ''
        count = 1
        with pymupdf.open(path) as pdf:
            for index, page in enumerate(pdf):
                count += 1
                pdf_text += page.get_text() + '\x0c'
        data_dict['text'] = pdf_text
        data_dict['page_start'] = 1
        data_dict['page_end'] = count
        return data_dict
