from enum import Enum


class CargoType(str, Enum):
    """
    Тип (размер) кузова для грузового тарифа.
    Точный список возможных значений для конкретной геоточки уточните с помощью метода получения тарифов v2/tariffs
    """
    VAN = "van"
    LCV_M = "lcv_m"
    LCV_L = "lcv_l"
