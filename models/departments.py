from typing_extensions import Annotated
from pydantic import BaseModel, Field, field_validator


class DepartmentsSchema(BaseModel):
    departments: Annotated[list[dict], Field(description="Массив, содержащий JSON-объекты с департаментами")]

    @field_validator("departments", mode="before")
    def check_departments(cls, value):
        if not isinstance(value, list):
            raise TypeError("departments должно быть списком")

        for elem in value:

            if not isinstance(elem, dict):
                raise TypeError("Элементы списка departments должны быть словарями!")

            if "departmentId" not in elem:
                raise ValueError("В словарях должен присутствовать ключ departmentId")

            if "displayName" not in elem:
                raise ValueError("В словарях должен присутствовать ключ displayName")

            if not len(elem) == 2:
                raise TypeError("В словарях должно быть два элемента!")

            if not isinstance(elem.get("departmentId", None), int):
                raise TypeError("Значение по ключу departmentId в словаре должно быть целочисленным!")

            if not isinstance(elem.get("displayName", None), str):
                raise TypeError("Значение по ключу displayName в словаре должно быть строковым!")

        return value
