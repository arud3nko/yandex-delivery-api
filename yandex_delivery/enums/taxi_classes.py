from enum import Enum


class TaxiClasses(str, Enum):
    """
    Класс автомобиля для доставки.
    Возможные значения: courier, express, cargo.

    Точный список возможных значений для конкретной точки уточните с помощью метода получения тарифов v2/tariffs
    """
    COURIER = "courier"
    EXPRESS = "express"
    CARGO = "cargo"
