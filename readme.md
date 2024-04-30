
# yandex-delivery
![Static Badge](https://img.shields.io/badge/API-v2-green?style=flat-square)
![Static Badge](https://img.shields.io/badge/master-v1.0.4-green?style=flat-square&logo=github)
![PyPI - Version](https://img.shields.io/pypi/v/yandex-delivery-api?style=flat-square&logo=pypi&logoColor=yellow&color=darkgoldenrod)

![Static Badge](https://img.shields.io/badge/status-WIP-yellow?style=flat)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-pr/arud3nko/yandex-delivery-api?style=flat-square)

![GitHub Repo stars](https://img.shields.io/github/stars/arud3nko/yandex-delivery-api)

Эта библиотека является Python оберткой для API Яндекс.Доставки.

## Features

- Асинхронный код. Синхронный будет поддерживаться позднее
- Покрытие часто используемых методов API
- Строгая аннотация типов
- Код документирован с полезными ссылками
- Подсказки в IDE


### О несоответствии новой документации API Яндкес Доставки
В данный момент существует две версии документаций к сервису доставки:
- Старая версия
```
https://yandex.com/dev/logistics/api/ref/basic.html
```
- Новая версия
```
https://yandex.ru/support2/delivery-profile/ru/api/express/overview
```

Библиотека разрабатывалась, когда старая версия документации была основной, однако сейчас все пути ведут на новую версию. 

Однако, старые методы и модели данных работают и остаются актуальными.

Я продолжаю доработку библиотеки в соответствии с новой версией документации, изменения постепенно вносятся.

Методы и модели данных, соответсвующие новой документации доступны в модулях:
```yandex_delivery.api_v2```, ```yandex_delivery.types.v2```


## Installation

Установите, клонировав репозиторий и установив зависимости из файла requirements.txt

```
git clone https://github.com/arud3nko/yandex-delivery-api
```
```
pip install -r requirements.txt
```
    
## Usage example (старая версия)

```python
import asyncio

from yandex_delivery import YandexDeliveryApi
from yandex_delivery.types import Address, Contact, RoutePoint, Claim, ClientRequirements, Item, ItemSize


async def main():
    item_size = ItemSize(height=0.45, length=0.45, width=0.45)
    item_to_deliver = Item(title="This is just a test",
                           quantity=1,
                           cost_value=10,
                           size=item_size,
                           weight=0.98,
                           droppof_point=2,
                           pickup_point=1)

    rest_address = Address(coordinates=(92.841019, 56.009552),
                           fullname="Красноярск, улица Карла Маркса, 134")
    rest_admin = Contact(name="Anthony", phone="+79839876543")
    restaurant = RoutePoint(address=rest_address, contact=rest_admin,
                            point_id=1,
                            type="source",
                            visit_order=1)

    client_contact = Contact(name="Anatoly", phone="+79981234567")
    client_address = Address(coordinates=(92.9993, 56.01189),
                             fullname="Красноярск, улица Красной Армии, 21")

    client = RoutePoint(address=client_address,
                        contact=client_contact,
                        point_id=2,
                        type="destination",
                        visit_order=2)

    client_requirements = ClientRequirements(cargo_options=["thermobag", "auto_courier"],
                                             taxi_class="express")

    items = [item_to_deliver]

    route_points = [restaurant, client]

    claim = Claim(items=items, route_points=route_points, client_requirements=client_requirements)

    async with YandexDeliveryApi(api_key="1234567890abcdefg") as api:
        result = await api.create(claim)
        print(result.data)

if __name__ == '__main__':
    asyncio.run(main())
```

## Documentation

```python
    async def create(self,
                     claim: Claim) -> Result:
        """
        Request to /claims/create method

        :param claim: Claim object

        https://yandex.ru/dev/logistics/api/ref/basic/IntegrationV2ClaimsCreate.html
        """
    
    async def check_price(self,
                          claim: Claim) -> Result:
        """
        Request to /check-price method

        :param claim: Claim object

        https://yandex.ru/dev/logistics/api/ref/estimate/IntegrationV2CheckPrice.html
        """
    
    async def accept(self,
                     claim_id: str,
                     version: int = 1) -> Result:
        """
        Request to /claims/accept

        :param claim_id: Claim ID
        :param version: Claim version. 1 by default (claim was not edited)

        https://yandex.ru/dev/logistics/api/ref/basic/IntegrationV2ClaimsAccept.html
        """

    async def info(self,
                   claim_id: str) -> Result:
        """
        Request to /claims/info method

        :param claim_id: Claim ID

        https://yandex.ru/dev/logistics/api/ref/basic/IntegrationV2ClaimsInfo.html
        """

    async def cancel_info(self,
                          claim_id: str) -> Result:
        """
        Request to /claims/cancel-info method

        :param claim_id: Claim ID

        https://yandex.ru/dev/logistics/api/ref/cancel-and-skip-points/IntegrationV2ClaimsCancelInfo.html
        """

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

    async def driver_voiceforwarding(self,
                                     claim_id: str,
                                     point_id: int = None) -> Result:
        """
        Request to /driver_voiceforwarding method

        :param claim_id: Claim ID
        :param point_id: Point ID (generated by Delivery)

        https://yandex.ru/dev/logistics/api/ref/performer-info/IntegrationV2DriverVoiceForwarding.html
        """

    async def performer_position(self,
                                 claim_id: str) -> Result:
        """
        Request to /performer_position method

        :param claim_id: Claim ID

        https://yandex.ru/dev/logistics/api/ref/performer-info/IntegrationV2ClaimsPerformerPosition.html
        """

    async def tracking_links(self,
                             claim_id: str) -> Result:
        """
        Request to /tracking-links method

        :param claim_id: Claim ID

        https://yandex.ru/dev/logistics/api/ref/performer-info/IntegrationV2ClaimsTrackingLinks.html
        """ 
    
```


## Authors

- [@arud3nko](https://www.github.com/arud3nko)


## License

[MIT](https://opensource.org/license/mit/)

