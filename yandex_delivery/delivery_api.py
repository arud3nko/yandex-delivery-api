import asyncio
import logging

from .models import Claim
from .rest_adapter import RestAdapter
from .exceptions import YandexDeliveryApiError
from .rest_result import Result


class YandexDeliveryApi:
    def __init__(self,
                 hostname: str = "b2b.taxi.yandex.net/b2b/cargo/integration",
                 api_key: str = "",
                 ver: str = "v2",
                 content_type: str = "'content-type': 'application/json', 'Accept-Language': 'ru'",
                 logger: logging.Logger = None):
        self._rest_adapter = RestAdapter(hostname=hostname,
                                         api_key=api_key,
                                         ver=ver,
                                         content_type=content_type,
                                         logger=logger)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def create(self,
                     claim: Claim) -> ...:
        # print(claim.model_dump(mode="dict", exclude_none=True))
        return await self._rest_adapter.get(endpoint="/claims/create",  # TODO исправлять -- aiohttp не читает ни json, ни dict
                                            params=claim.model_dump(mode="json", exclude_none=True))
