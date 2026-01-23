from typing_extensions import Annotated
from pydantic import BaseModel, Field, field_validator


class DepartmentsSchema(BaseModel):
    """
    Pydantic схема для валидации структуры ответа API departments.

    Ожидаемая структура:
    {
        "departments": [
            {
                "departmentId": int,
                "displayName": str
            }
        ]
    }
    """

    departments: Annotated[list[dict], Field(description="Массив с департаментами")]

    @field_validator("departments", mode="before")
    def check_departments(cls, value):
        """
        Валидатор для проверки структуры массива departments.

        Args:
            value: Значение поля departments для валидации

        Returns:
            Проверенный и нормализованный массив departments

        Raises:
            TypeError: Если нарушены требования к типам данных
            ValueError: Если отсутствуют обязательные поля
        """
        if not isinstance(value, list):
            raise TypeError("departments должно быть списком")

        for elem in value:
            if not isinstance(elem, dict):
                raise TypeError("Элементы списка departments должны быть словарями")

            if "departmentId" not in elem:
                raise ValueError("В словарях должен присутствовать ключ departmentId")

            if "displayName" not in elem:
                raise ValueError("В словарях должен присутствовать ключ displayName")

            if not len(elem) == 2:
                raise TypeError("В словарях должно быть два элемента")

            if not isinstance(elem.get("departmentId", None), int):
                raise TypeError("Значение по ключу departmentId должно быть целочисленным")

            if not isinstance(elem.get("displayName", None), str):
                raise TypeError("Значение по ключу displayName должно быть строковым")

        return value