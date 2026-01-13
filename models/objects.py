from typing_extensions import Annotated
from pydantic import BaseModel, Field, field_validator


class ObjectsSchema(BaseModel):
    total: Annotated[int, Field(ge=0, description="Общее количество объектов")]
    objectIDs: Annotated[list[int], Field(description="ID объектов")]

    @field_validator("total", mode="before")
    def check_total(cls, value):
        if isinstance(value, int):
            return value
        raise TypeError("total должно быть целочисленным!")

    @field_validator("objectIDs", mode="before")
    def check_objectids(cls, value):
        if not isinstance(value, list):
            raise TypeError("objectIDs должно быть списком!")

        for el in value:
            if not isinstance(el, int):
                raise TypeError("Все элементы в objectIDs должны быть целочисленные!")

        return value