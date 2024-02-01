import asyncio

from yandex_delivery import YandexDeliveryApi, Claim, Item, RoutePoint, ItemSize, Address, Contact


async def main():
    item_size = ItemSize(height=0.45, length=0.45, width=0.45)
    item_to_deliver = Item(title="тестовый заказ",
                           quantity=1,
                           cost_value=10,
                           size=item_size,
                           droppof_point=2,
                           pickup_point=1)

    rest_address = Address(coordinates=[56.009552, 92.841019],
                           fullname="Красноярск, улица Карла Маркса, 134")
    rest_admin = Contact(name="Егор", phone="89950802045")
    restaurant = RoutePoint(address=rest_address, contact=rest_admin,
                            point_id=1,
                            type="source",
                            visit_order=1)

    client_contact = Contact(name="Егор", phone="89950802045")
    client_address = Address(coordinates=[56.011735, 92.821015],
                             fullname="Красноярск, улица Копылова, 19")

    client = RoutePoint(address=client_address,
                        contact=client_contact,
                        point_id=2,
                        type="destination",
                        visit_order=2)

    items = [item_to_deliver]

    route_points = [restaurant, client]

    claim = Claim(items=items, route_points=route_points)



    async with YandexDeliveryApi() as api:
        result = await api.create(claim=claim)

        print(result)


if __name__ == '__main__':
    asyncio.run(main())