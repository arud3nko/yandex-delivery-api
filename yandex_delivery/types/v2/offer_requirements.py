from __future__ import annotations

from typing import Optional, List, Literal

from typing_extensions import Annotated

from datetime import datetime

from pydantic import Field

from .base import MutableDeliveryObject
from ..enums import TaxiClasses, CargoType, CargoOptions


class OfferRequirements(MutableDeliveryObject):
    """
    Требования к доставке

    Source: https://yandex.ru/support2/delivery-profile/ru/api/express/openapi/IntegrationV2OfferCalculate#offerrequirements
    """
    taxi_classes: Optional[List[Literal[TaxiClasses.CARGO, TaxiClasses.COURIER, TaxiClasses.EXPRESS]]] = None
    """Класс автомобиля для доставки. Возможные значения: courier, express, cargo.
    Точный список возможных значений для конкретной точки уточните с помощью метода получения тарифов v2/tariffs"""
    cargo_type: Optional[List[Literal[CargoType.VAN, CargoType.LCV_M, CargoType.LCV_L]]] = None
    """Тип (размер) кузова для грузового тарифа. Возможные значения:
    van ("Маленький кузов"), lcv_m ("Средний кузов"), lcv_l ("Большой кузов"). 
    Точный список возможных значений для конкретной точки уточните с помощью метода получения тарифов v2/tariffs"""
    cargo_loaders: Optional[Annotated[int, Field(ge=0, le=2)]] = None
    """Число грузчиков для грузового тарифа. Возможные значения: 0, 1, 2.
    Точный список возможных значений для конкретной точки уточните с помощью метода получения тарифов v2/tariffs"""
    pro_courier: Optional[bool] = None
    """Опция "Профи" для тарифов "Экспресс" и "Курьер" """
    cargo_options: Optional[List[Literal[CargoOptions.AUTO_COURIER, CargoOptions.THERMOBAG]]] = None
    """Список дополнительных опций тарифа. Возможные отдельные опции:
    auto_courier (курьер только на машине), thermobag (курьер с термосумкой)
    Точный список возможных значений для конкретной геоточки уточните с помощью метода получения тарифов v1/tariffs"""
    skip_door_to_door: Optional[bool] = None
    """Отказ от доставки до двери (выключить опцию "От двери до двери").
    Возможные значения: true (курьер доставит заказ только на улицу, до подъезда),
    false (по умолчанию, доставка от двери до двери)"""
    due: Optional[datetime] = None
    """Ожидаемое время подачи (отложить ожидаемое время подачи можно на 30-60 минут от текущего момента)"""
