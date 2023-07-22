from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema
from pydantic_core.core_schema import ValidationInfo


class EntityID(str):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, *agrs, **kwargs  # pylint: disable=W0613
    ) -> JsonSchemaValue:
        json_schema: dict[str, Any] = {}
        json_schema.update(type="string")
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, *args, **kwargs) -> CoreSchema:
        return core_schema.general_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v: str | UUID | EntityID, info: ValidationInfo):
        error_message = f"{v} isnt a valid UUID"
        if isinstance(v, EntityID):
            return v

        if isinstance(v, UUID):
            return str(v)

        if not isinstance(v, str):
            raise ValueError(error_message)

        try:
            UUID(v)
        except Exception as e:
            raise ValueError(error_message) from e

        return v

    @classmethod
    def new(cls) -> EntityID:
        return cls(uuid4())
