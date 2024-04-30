from __future__ import annotations

from typing import Tuple, Optional

from .base import MutableDeliveryObject


class RoutePointWithAddress(MutableDeliveryObject):
    """
    Точка маршрута

    Source: https://yandex.ru/support2/delivery-profile/ru/api/express/openapi/IntegrationV2OfferCalculate#routepointwithaddress
    """
    id:          Optional[int] = None
    """Числовой id точки(int64). Для работы с мультиточками ОБЯЗАТЕЛЕН к заполнению"""
    coordinates: Optional[Tuple[float, float]] = None
    """Массив из двух вещественных чисел [долгота, широта]. Порядок важен!"""
    fullname:    Optional[str] = None
    """Полное название с указанием города (Москва, Садовническая набережная, 82с2).
    Важно вводить населенный пункт с указанием номера дома, но без номера квартиры, подъезда, этажа"""
