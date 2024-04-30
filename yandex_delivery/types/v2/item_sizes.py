from __future__ import annotations

from pydantic import NonNegativeFloat

from .base import MutableDeliveryObject


class ItemSizes(MutableDeliveryObject):
    """
    Линейные размеры предмета в метрах.
    Пример: 0.45

    Source: https://yandex.ru/support2/delivery-profile/ru/api/express/openapi/IntegrationV2OfferCalculate#itemsizes

    """
    height: NonNegativeFloat
    length: NonNegativeFloat
    width:  NonNegativeFloat
