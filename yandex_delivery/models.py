"""

This module describes Yandex Delivery API models

"""
from typing import Optional, Literal, List, Tuple

from pydantic import (BaseModel, PositiveInt, NonNegativeFloat, Field, HttpUrl, NonNegativeInt, StrictBool, StrictFloat
                      )
from typing_extensions import Annotated


class Contact(BaseModel):
    pass


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
    address: Address
    buyout: Optional[Buyout] = None



class EmergencyContact(BaseModel):
    """

    This class describes delivery customer contact

    """
    name:                  Annotated[str, Field(min_length=1)]
    phone:                 Annotated[str, Field(min_length=1)]
    phone_additional_code: Optional[str] = None


class ClientRequirements(BaseModel):
    """

    This class describes client requirements, these requirements are necessary to create or edit claim

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
    cost_value:    NonNegativeFloat
    size:          ItemSize
    droppof_point: NonNegativeInt
    pickup_point:  NonNegativeInt
    cost_currency: Annotated[str, Field(default="RUB", min_length=1)]
    extra_id:      Optional[str] = None
    fiscalization: Optional[str] = None


class Claim(BaseModel):
    """

    This class describes delivery claim

    """
    auto_accept:           Optional[StrictBool] = None
    callback_properties:   Optional[CallbackProperties] = None
    client_requirements:   Optional[ClientRequirements] = None
    comment:               Optional[str] = None
    due:                   None  # TODO
    emergency_contact:     Optional[EmergencyContact] = None
    items:                 List[Item]
    offer_payload:         Optional[str] = None
    optional_return:       Optional[StrictBool] = None
    referral_source:       Optional[str] = None
    route_points:          List[None]  # TODO
    same_day_data:         None  # TODO
    shipping_document:     Optional[str] = None
    skip_act:              Optional[StrictBool] = None
    skip_client_notify:    Optional[StrictBool] = None
    skip_door_to_door:     Optional[StrictBool] = None
    skip_emergency_notify: Optional[StrictBool] = None
