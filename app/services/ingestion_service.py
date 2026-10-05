class IngestionService:

    def __init__(self, etl_pipeline):
        self.etl_pipeline = etl_pipeline

    def ingest(self, source: str):
        self.etl_pipeline.process(source)