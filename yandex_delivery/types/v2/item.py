from __future__ import annotations

from typing import Optional

from pydantic import PositiveInt, NonNegativeInt, NonNegativeFloat

from .base import MutableDeliveryObject
from .item_sizes import ItemSizes


class Item(MutableDeliveryObject):
    """
    Параметры предмета

    Source: https://yandex.ru/support2/delivery-profile/ru/api/express/openapi/IntegrationV2OfferCalculate#item
    """
    size:          Optional[ItemSizes] = None
    """Линейные размеры предмета в метрах."""
    weight:        Optional[NonNegativeFloat] = None
    """Вес в килограммах."""
    quantity:      Optional[PositiveInt] = None
    """Количество единиц товара"""
    pickup_point:  Optional[NonNegativeInt] = None
    """Идентификатор точки(int64), откуда нужно забрать товар.
    Может быть любым числом. Должен соответствовать значению route_points[].id у точки забора.
    Обязательно передать для работы с мультиточками."""
    dropoff_point: Optional[NonNegativeInt] = None
    """Идентификатор точки(int64), куда нужно доставить товар.
    Может быть любым числом. Должен соответствовать значению route_points[].id у точки назначения.
    Обязательно передать для работы с мультиточками."""
