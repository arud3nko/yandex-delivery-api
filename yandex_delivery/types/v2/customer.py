from __future__ import annotations

from typing import Optional

from pydantic_extra_types.phone_numbers import PhoneNumber
from typing_extensions import Annotated

from pydantic import BaseModel, EmailStr


class Customer(BaseModel):
    """

    This class describes customer. It's useful for on delivery payment

    """
    email: Optional[EmailStr] = None
    inn:   Optional[str] = None
    phone: Optional[Annotated[str, PhoneNumber]] = None
