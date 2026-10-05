from ETL.extract.base import BaseFileReader
import pymupdf


class PDFReader(BaseFileReader):

    def read(self, path) -> list[dict[str, str]]:
        data_list = []
        with pymupdf.open(path) as pdf:
            for index, page in enumerate(pdf):
                data_list.append({'page_number': index + 1, 'page': page.get_text()})
        return data_list
