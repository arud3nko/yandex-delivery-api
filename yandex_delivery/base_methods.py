"""

This module describes API objects for API Base Methods

"""
from typing import Optional, Literal, List, Tuple
from typing_extensions import Annotated

from pydantic import (BaseModel, PositiveInt, NonNegativeFloat,
                      Field, HttpUrl, NonNegativeInt,
                      StrictBool, EmailStr, field_validator)
from pydantic_extra_types.phone_numbers import PhoneNumber


class Customer(BaseModel):
    """

    This class describes customer. It's useful for on delivery payment

    """
    email: Optional[EmailStr] = None
    inn:   Optional[str] = None
    phone: Optional[Annotated[str, PhoneNumber]] = None


class PaymentOnDelivery(BaseModel):
    """

    This class describes on delivery payment info

    """
    customer:       Optional[Customer] = None
    payment_method: Literal["card", "cash"]


class ExternalOrderCost(BaseModel):
    """

    This class describes external order cost

    """
    currency:      Annotated[str, Field(min_length=1)]
    currency_sign: Annotated[str, Field(min_length=1)]
    value:         Annotated[str, Field(min_length=1)]


class Contact(BaseModel):
    """

    This class describes contact person

    """
    email:                 Optional[EmailStr] = None
    name:                  Annotated[str, Field(min_length=1)]
    phone:                 Annotated[str, PhoneNumber]
    phone_additional_code: Optional[str] = None


class Buyout(BaseModel):
    """

    This class describes chosen buyout type

    """
    payment_method: Literal["card", "cash"]


class Address(BaseModel):
    """

    This class describes address fields

    """
    building:        Optional[str] = None
    building_name:   Optional[str] = None
    city:            Optional[str] = None
    comment:         Optional[str] = None
    coordinates:     Tuple[float, float]
    country:         Optional[str] = None
    description:     Optional[str] = None
    door_code:       Optional[str] = None
    door_code_extra: Optional[str] = None
    doorbell_name:   Optional[str] = None
    fullname:        Annotated[str, Field(min_length=1)]
    porch:           Optional[str] = None
    sflat:           Optional[str] = None
    sfloor:          Optional[str] = None
    shortname:       Optional[str] = None
    street:          Optional[str] = None
    uri:             Optional[str] = None


class RoutePoint(BaseModel):
    """

    This class describes route point parameters

    """
    address:             Address
    buyout:              Optional[Buyout] = None
    contact:             Contact
    external_order_cost: Optional[ExternalOrderCost] = None
    external_order_id:   Optional[str] = None
    leave_under_door:    Optional[StrictBool] = None
    meet_outside:        Optional[StrictBool] = None
    no_door_call:        Optional[StrictBool] = None
    payment_on_delivery: Optional[PaymentOnDelivery] = None
    pickup_code:         Optional[Annotated[str, Field(min_length=6, max_length=6)]] = None
    point_id:            int  # int64
    skip_confirmation:   Optional[StrictBool] = None
    type:                Literal["source", "destination", "return"]
    visit_order:         PositiveInt


class EmergencyContact(BaseModel):
    """

    This class describes delivery customer contact

    """
    name:                  Annotated[str, Field(min_length=1)]
    phone:                 Annotated[str, PhoneNumber]
    phone_additional_code: Optional[str] = None


class ClientRequirements(BaseModel):
    """

    This class describes client requirements, these requirements are
    necessary to create or edit claim

    """
    assign_robot:  Optional[StrictBool] = None
    cargo_loaders: Optional[Literal[0, 1, 2]] = None
    cargo_options: Optional[List[Literal["thermobag", "auto_courier"]]] = None
    cargo_type:    Optional[Literal["van", "lcv_m", "lcv_l"]] = None
    pro_courier:   Optional[StrictBool] = None
    taxi_class:    Literal["courier", "express", "cargo"]


class CallbackProperties(BaseModel):
    """

    This class describes callback URL for API to send claim status

    """
    callback_url: Optional[HttpUrl] = None


class ItemSize(BaseModel):
    """

    This class describes item size in meters

    """
    height: NonNegativeFloat
    length: NonNegativeFloat
    width:  NonNegativeFloat


class Item(BaseModel):
    """

    This class describes item to delivery
    All integer values should be int64

    """
    title:         Annotated[str, Field(min_length=1)]
    quantity:      PositiveInt
    cost_value:    Annotated[str | float, Field(ge=0)]
    size:          ItemSize
    droppof_point: NonNegativeInt
    pickup_point:  NonNegativeInt
    cost_currency: Annotated[str, Field(default="RUB", min_length=1)] = "RUB"
    extra_id:      Optional[str] = None
    fiscalization: Optional[str] = None
    weight:        Optional[NonNegativeFloat] = None

    @field_validator("cost_value", mode="before")
    def convert_to_float(cls, value):
        """
        Any to float
        """
        if not isinstance(value, float):
            return float(value)
        return value

    @field_validator("cost_value", mode="after")
    def convert_to_string(cls, value):
        """
        Any to string
        """
        return str(value)


class Claim(BaseModel):
    """

    This class describes delivery claim

    """
    auto_accept:           Optional[StrictBool] = None
    callback_properties:   Optional[CallbackProperties] = None
    client_requirements:   Optional[ClientRequirements] = None
    comment:               Optional[str] = None
    due:                   None = None  # TODO
    emergency_contact:     Optional[EmergencyContact] = None
    items:                 Optional[List[Item]] = None
    offer_payload:         Optional[str] = None
    optional_return:       Optional[StrictBool] = None
    referral_source:       Optional[str] = None
    route_points:          List[RoutePoint]
    same_day_data:         None = None  # TODO
    shipping_document:     Optional[str] = None
    skip_act:              Optional[StrictBool] = None
    skip_client_notify:    Optional[StrictBool] = None
    skip_door_to_door:     Optional[StrictBool] = None
    skip_emergency_notify: Optional[StrictBool] = None
