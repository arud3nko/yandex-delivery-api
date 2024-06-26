from typing import Any, Dict
from unittest.mock import sentinel

from pydantic import BaseModel, ConfigDict, model_validator


class DeliveryObject(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        extra="allow",
        validate_assignment=True,
        frozen=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        defer_build=True,
    )

    @classmethod
    @model_validator(mode="before")
    def remove_unset(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove UNSET before fields validation.
        """
        if not isinstance(values, dict):
            return values
        return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}


class MutableDeliveryObject(DeliveryObject):
    model_config = ConfigDict(
        frozen=False,
    )


UNSET: Any = sentinel.UNSET
UNSET_TYPE: Any = type(UNSET)
