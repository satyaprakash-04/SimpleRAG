import uuid
from typing import Any

from ETL.extract.base import BaseExtractor, BaseTransformer
from ETL.embed.embedder import DocumentEmbedder
from ETL.load.load import BaseLoader
from app.models.chunk import DocumentChunk


class ETLPipeline:

    def __init__(
        self,
        extractor: BaseExtractor,
        transformer: BaseTransformer,
        embedder: DocumentEmbedder,
        loader: BaseLoader,
    ):
        self.extractor = extractor
        self.transformer = transformer
        self.embedder = embedder
        self.loader = loader

    def run(
            self,
            data_source: str,
        ) -> None:
        extracted_data = self.extractor.extract_details(path=data_source)
        for data in extracted_data:
            doc_data_list = []
            for page_info in data['pdf_data']:
                doc_id = uuid.uuid4()
                prepared_dict: dict[str, Any] = {
                    'file_path': '{data_source}/{file_name}'.format(
                        data_source=data_source,
                        file_name=data['file_name']
                    ),
                    'file_name': data['file_name'],
                    'extension': data['extension'],
                    'page_number': page_info['page_number'],
                    'page_data': page_info['page']
                }
                transformed_page_chunk: list[DocumentChunk] = self.transformer.transform(
                    document=prepared_dict,
                    document_id=doc_id,
                )
                self.embedder.embed(transformed_page_chunk)
                prepared_dict['embeddings'] = transformed_page_chunk
                doc_data_list.append(prepared_dict)
                loader = self.loader.load(
                    document_id=doc_id,
                    file_name=prepared_dict['file_name'],
                    file_path=prepared_dict['file_path'],
                    extension=prepared_dict['extension'],
                    chunks=transformed_page_chunk
                )



