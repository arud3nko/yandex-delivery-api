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
    