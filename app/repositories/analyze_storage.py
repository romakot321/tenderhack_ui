from app.schemas.analyze import AnalyzeSchema


class AnalyzeStorageRepository:
    models = []
    cached_urls = {}

    def __init__(self):
        pass

    def store(self, model: AnalyzeSchema, url: str):
        self.models.append(model)
        self.cached_urls[url] = model
        return model

    def get(self, url: str) -> AnalyzeSchema | None:
        return self.cached_urls.get(url)

