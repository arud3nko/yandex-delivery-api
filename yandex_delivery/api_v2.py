"""

This module describes API class

"""
from __future__ import annotations

import logging
import uuid

from typing import Literal, List, Optional

from yandex_delivery.types import Claim
from yandex_delivery.types.v2 import Item, RoutePointWithAddress, OfferRequirements

from .rest import RestAdapter, Result


class YandexDeliveryApi:
    """

    This class describes Delivery API object

    """
    def __init__(self,
                 hostname:        str = "b2b.taxi.yandex.net/b2b/cargo/integration",
                 api_key:         str = "",
                 ver:             str = "v2",
                 content_type:    str = "application/json",
                 accept_language: str = "ru",
                 retries:         int = 0,
                 timeout:         Optional[int] = 5,
                 logger:          Optional[logging.Logger] = None):
        self._rest_adapter = RestAdapter(hostname=hostname,
                                         api_key=api_key,
                                         ver=ver,
                                         content_type=content_type,
                                         accept_language=accept_language,
                                         retries=retries,
                                         timeout=timeout,
                                         logger=logger)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def create(self,
                     claim: Claim) -> Result:
        """
        Request to /claims/create method

        :param claim: Claim object

        https://yandex.ru/dev/logistics/api/ref/basic/IntegrationV2ClaimsCreate.html
        """
        return await self._rest_adapter.post(endpoint="/claims/create",
                                             payload=claim.model_dump(mode="json",
                                                                      exclude_none=True),
                                             params={"request_id": str(uuid.uuid4())})

    async def check_price(self,
                          claim: Claim) -> Result:
        """
        Request to /check-price method

        :param claim: Claim object

        https://yandex.ru/dev/logistics/api/ref/estimate/IntegrationV2CheckPrice.html
        """
        return await self._rest_adapter.post(endpoint="/check-price",
                                             payload=claim.model_dump(mode="json",
                                                                      exclude_none=True))

    async def accept(self,
                     claim_id: str,
                     version: int = 1) -> Result:
        """
        Request to /claims/accept

        :param claim_id: Claim ID
        :param version: Claim version. 1 by default (claim was not edited)

        https://yandex.ru/dev/logistics/api/ref/basic/IntegrationV2ClaimsAccept.html
        """
        return await self._rest_adapter.post(endpoint="/claims/accept",
                                             params={"claim_id": claim_id},
                                             payload={"version": version})

    async def info(self,
                   claim_id: str) -> Result:
        """
        Request to /claims/info method

        :param claim_id: Claim ID

        https://yandex.ru/dev/logistics/api/ref/basic/IntegrationV2ClaimsInfo.html
        """
        return await self._rest_adapter.post(endpoint="/claims/info",
                                             params={"claim_id": claim_id})

    async def cancel_info(self,
                          claim_id: str) -> Result:
        """
        Request to /claims/cancel-info method

        :param claim_id: Claim ID

        https://yandex.ru/dev/logistics/api/ref/cancel-and-skip-points/IntegrationV2ClaimsCancelInfo.html
        """
        return await self._rest_adapter.post(endpoint="/claims/cancel-info",
                                             params={"claim_id": claim_id})

    async def cancel(self,
                     claim_id: str,
                     cancel_state: Literal["free", "paid"],
                     version: int = 1) -> Result:
        """
        Request to /claims/cancel method

        :param claim_id: Claim ID
        :param cancel_state: Cancelling status. Enum: ["free", "paid"]
        :param version: Claim version. 1 by default (claim was not edited)

        https://yandex.ru/dev/logistics/api/ref/cancel-and-skip-points/IntegrationV2ClaimsCancelInfo.html
        """
        return await self._rest_adapter.post(endpoint="/claims/cancel",
                                             params={"claim_id": claim_id},
                                             payload={"cancel_state": cancel_state,
                                                      "version": version})

    async def driver_voiceforwarding(self,
                                     claim_id: str,
                                     point_id: int = None) -> Result:
        """
        Request to /driver_voiceforwarding method

        :param claim_id: Claim ID
        :param point_id: Point ID (generated by Delivery)

        https://yandex.ru/dev/logistics/api/ref/performer-info/IntegrationV2DriverVoiceForwarding.html
        """
        return await self._rest_adapter.post(endpoint="/driver-voiceforwarding",
                                             payload={"claim_id": claim_id,
                                                      "point_id": point_id} if point_id
                                             else {"claim_id": claim_id})

    async def performer_position(self,
                                 claim_id: str) -> Result:
        """
        Request to /performer_position method

        :param claim_id: Claim ID

        https://yandex.ru/dev/logistics/api/ref/performer-info/IntegrationV2ClaimsPerformerPosition.html
        """
        return await self._rest_adapter.get(endpoint="/claims/performer-position",
                                            params={"claim_id": claim_id})

    async def tracking_links(self,
                             claim_id: str) -> Result:
        """
        Request to /tracking-links method

        :param claim_id: Claim ID

        https://yandex.ru/dev/logistics/api/ref/performer-info/IntegrationV2ClaimsTrackingLinks.html
        """
        return await self._rest_adapter.get(endpoint="/claims/tracking-links",
                                            params={"claim_id": claim_id})

    async def calculate(self,
                        route_points: List[RoutePointWithAddress],
                        items:        List[Item] = None,
                        requirements: OfferRequirements = None):
        """
        Получение вариантов доставки (для РФ)
        Метод возвращает доступные варианты доставки.
        Каждый вариант содержит цену, временной интервал забора посылки на точке А,
        временной интервал доставки на точку B.
        После получения вариантов доставки можно выбрать оптимальный и создать заказ с
        использованием выбранного варианта.
        Получить варианты доставки можно только в России.

        Source: https://yandex.ru/support2/delivery-profile/ru/api/express/openapi/IntegrationV2OfferCalculate
        """
        return await self._rest_adapter.post(endpoint="/offers/calculate",
                                             payload={"items": items,
                                                      "route_points": [x.model_dump(mode="json", exclude_none=True)
                                                                       for x in route_points],
                                                      "requirements": requirements.model_dump(mode="json",
                                                                                              exclude_none=True)})
