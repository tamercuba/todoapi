from uuid import uuid4

import pytest
from click import UUID
from pydantic import ValidationError

from src.domain.entities.base import Entity
from src.domain.entities.base.id import EntityID


class DummyEntity(Entity):
    field: str


class DummiestEntity(Entity):
    field: str


class TestBaseEntity:
    def test_generated_id_successfully(self):
        entity = DummyEntity(field="a")
        assert entity.id

    def test_setting_custom_id_successfully(self):
        _id = EntityID.new()
        entity = DummyEntity(id=_id, field="a")
        assert entity.id == _id

    def test_cant_change_entity_id(self):
        entity = DummyEntity(field="a")

        with pytest.raises(ValidationError) as e:
            entity.id = uuid4()

        assert len(e.value.errors()) == 1

        error = e.value.errors()[0]
        assert error["type"] == "frozen_field"
        assert error["loc"][0] == "id"

    @pytest.mark.parametrize(
        "entity_a,entity_b,expected",
        [
            (
                DummyEntity(id="5fd6ca3a568a4afab3543d7d77ce5f84", field="a"),
                DummyEntity(id="5fd6ca3a568a4afab3543d7d77ce5f84", field="b"),
                True,
            ),
            (DummyEntity(field="a"), DummyEntity(field="a"), False),
            (
                DummyEntity(id="5fd6ca3a568a4afab3543d7d77ce5f84", field="a"),
                DummiestEntity(
                    id="5fd6ca3a568a4afab3543d7d77ce5f84", field="a"
                ),
                False,
            ),
        ],
    )
    def test_equality_operator(self, entity_a, entity_b, expected):
        assert (entity_a == entity_b) == expected


class TestEntityIdType:
    def test_cast_from_string_successfully(self):
        uuid = "ad53cf8c-5027-48a4-b464-bf0aa06b59ef"
        assert DummyEntity(id=uuid, field="").id == uuid

    def test_cast_from_random_string(self):
        with pytest.raises(ValidationError) as e:
            DummyEntity(id="a", field="b")

        error = e.value.errors()[0]
        assert error["type"] == "value_error"
        assert error["loc"][0] == "id"

    def test_cast_from_uuid_object(self):
        id = uuid4()

        assert DummyEntity(id=id, field="").id == str(id)

    def test_cant_cast_non_str_formats(self):
        with pytest.raises(ValidationError) as e:
            DummyEntity(id=1, field="")

        error = e.value.errors()[0]
        assert error["type"] == "value_error"
        assert error["loc"][0] == "id"
