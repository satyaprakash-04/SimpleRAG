from collections.abc import Iterator

from ETL.extract.base import BaseFileReader


class DocsReader(BaseFileReader):
    def read(self, path) -> list[dict[str, str]]:
        data_list = []
        for index, page in enumerate(path):
            data_list.append({'index': index, 'page': page})
        return data_list