import os
import aiohttp
from app.schemas.analyze import AnalyzeSchema
from app.schemas.user import CheckCriteriaSchema


class AnalyzeRepository:
    api_url = os.getenv("API_URL", "http://localhost:8002")

    async def _do_request(self, method: str, path: str, body: dict | None = None) -> dict:
        async with aiohttp.ClientSession(self.api_url) as session:
            if method == "POST":
                response = await session.post(path, json=body)
            elif method == "GET":
                response = await session.get(path)
            assert response.status // 100 == 2
            result = await response.json()
        return result

    async def create_auction_analyze(self, url: str, criteria: CheckCriteriaSchema) -> AnalyzeSchema:
        resp = await self._do_request(
            'POST',
            '/api/auction/url',
            {
                'url': url,
                'criteria': [name for name, value in criteria.model_dump().items() if value]
            }
        )
        return AnalyzeSchema.model_validate(resp)

    async def check_auction_analyze(self, analyze_id: int) -> AnalyzeSchema | None:
        try:
            resp = await self._do_request('GET', f'/api/auction/qs/{analyze_id}')
        except AssertionError:
            return
        return AnalyzeSchema.model_validate(resp)
