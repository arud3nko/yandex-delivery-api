from enum import Enum


class CargoOptions(str, Enum):
    """
    Список дополнительных опций тарифа.

    Возможные отдельные опции:

    auto_courier (курьер только на машине)
    thermobag (курьер с термосумкой)

    Точный список возможных значений для конкретной геоточки уточните с помощью метода получения тарифов v1/tariffs
    """
    AUTO_COURIER = "auto_courier"
    THERMOBAG = "thermobag"
