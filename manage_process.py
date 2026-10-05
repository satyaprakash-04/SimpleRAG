import os

from ETL.embed.embedder import DocumentEmbedder
from ETL.extract.file_extractor import FileExtractor
from ETL.load.postgres_loader import PostgresLoader
from ETL.pipeline import ETLPipeline
from ETL.transform.chunker import RecursiveChunker
from ETL.transform.cleaner import TextCleaner
from ETL.transform.transformer import DocumentTransformer
from app.clients.sentense_transformer_client import SentenceTransformerClient
from database.connector import SessionLocal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cleaner =  TextCleaner()
chunker = RecursiveChunker()

extractor = FileExtractor(
    paths=os.path.join(BASE_DIR, 'datasource')
)
transformer = DocumentTransformer(
    cleaner=cleaner,
    chunker=chunker,
)
embedding_client = SentenceTransformerClient(
    model_name='all-MiniLM-L6-v2'
)
embeder = DocumentEmbedder(
    embedding_client=embedding_client
)
loader = PostgresLoader()

if __name__ == "__main__":
    pipeline = ETLPipeline(
        extractor=extractor,
        transformer=transformer,
        embedder=embeder,
        loader=loader,
    )
    pipeline.run(os.path.join(BASE_DIR, 'datasource'))

