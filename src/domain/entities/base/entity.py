from pydantic import BaseModel, ConfigDict, Field

from src.domain.entities.base.id import EntityID


class Entity(BaseModel):
    id: EntityID = Field(default_factory=EntityID.new, frozen=True)
    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True
    )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return self.id == __value.id

        return False
