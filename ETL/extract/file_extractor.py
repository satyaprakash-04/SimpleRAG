import re
from pathlib import Path

from ETL.extract.base import BaseExtractor, BaseFileReader
from ETL.extract.docs_reader import DocsReader
from ETL.extract.pdf_reader import PDFReader


class FileExtractor(BaseExtractor):
    def __init__(self, paths: str) -> None:
        self.path = paths
        self.mapper = {
            'pdf': PDFReader(),
            'docx': DocsReader(),
        }

    def extract_paths(self, paths: str) -> list[str]:
        path_list = []
        source_path = Path(paths)
        for file_path in source_path.rglob("*"):
            path_list.append(str(file_path))
        return path_list

    def extract_details(self, path: str) -> list[dict[str, str | list[dict[str, str]]]]:
        books_data = []
        for file in self.extract_paths(path):
            file_details = self.get_file_details(file)
            if file_details is not None:
                reader = self.get_reader(file_details)
                pdf_data =  reader.read(file)
                file_details['file_data'] = pdf_data
                books_data.append(file_details)
        return books_data

    @staticmethod
    def get_file_details(path: str) -> dict | None:
        pattern = r"([^/\\\\]+)\.([^./\\\\]+)$"

        match = re.search(pattern, path)
        if match:
            filename = match.group(1)
            extension = match.group(2)
            return {
                'file_name': filename + "." + extension,
                'extension': extension,
                'path': path
            }
        return None

    def get_reader(self, file_details: dict[str, str]) -> BaseFileReader:
        reader = self.mapper[file_details['extension']]
        return reader
