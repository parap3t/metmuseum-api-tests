import re

from datetime import datetime
from typing import List, Dict, Any, Optional, Annotated
from pydantic import BaseModel, Field, field_validator, ConfigDict


class ObjectSchema(BaseModel):
    """
    Pydantic схема для валидации данных объекта из API музея.

    Содержит полную информацию об объекте искусства, включая метаданные,
    изображения, информацию об авторе, географические данные и измерения.
    """

    model_config = ConfigDict(extra='ignore')

    # Основные идентификаторы и флаги
    objectID: Annotated[int, Field(ge=0, description="Уникальный идентификационный номер объекта")]
    isHighlight: Annotated[Optional[bool], Field(None, description="Флаг популярного объекта коллекции")]
    accessionNumber: Annotated[Optional[str], Field(None, description="Номер поступления объекта")]
    accessionYear: Annotated[Optional[str], Field(None, description="Год приобретения объекта музеем")]
    isPublicDomain: Annotated[Optional[bool], Field(None, description="Флаг нахождения в общественном достоянии")]

    # Изображения
    primaryImage: Annotated[Optional[str], Field(None, description="URL основного изображения")]
    primaryImageSmall: Annotated[Optional[str], Field(None, description="URL уменьшенного изображения")]
    additionalImages: Annotated[Optional[List[str]], Field(default=[], description="URL дополнительных изображений")]

    # Коллекции данных
    constituents: Annotated[Optional[List[Dict[str, Any]]], Field(default=[], description="Связанные лица и роли")]
    measurements: Annotated[Optional[List[Dict[str, Any]]], Field(default=[], description="Измерения объекта")]
    dimensionsParsed: Annotated[Optional[List[Dict[str, Any]]], Field(default=[], description="Размеры в сантиметрах")]
    tags: Annotated[Optional[List[Dict[str, Any]]], Field(default=[], description="Теги объекта")]

    # Классификация и описание
    department: Annotated[Optional[str], Field(None, description="Кураторский отдел музея")]
    objectName: Annotated[Optional[str], Field(None, description="Физический тип объекта")]
    title: Annotated[Optional[str], Field(None, description="Название произведения")]
    culture: Annotated[Optional[str], Field(None, description="Культура создания")]
    period: Annotated[Optional[str], Field(None, description="Временной период создания")]
    dynasty: Annotated[Optional[str], Field(None, description="Правящая династия")]
    reign: Annotated[Optional[str], Field(None, description="Правление монарха")]
    portfolio: Annotated[Optional[str], Field(None, description="Серия или группа")]

    # Информация об авторе
    artistRole: Annotated[Optional[str], Field(None, description="Роль автора")]
    artistPrefix: Annotated[Optional[str], Field(None, description="Квалификатор авторства")]
    artistDisplayName: Annotated[Optional[str], Field(None, description="Имя автора")]
    artistDisplayBio: Annotated[Optional[str], Field(None, description="Биография автора")]
    artistSuffix: Annotated[Optional[str], Field(None, description="Дополнительная информация")]
    artistAlphaSort: Annotated[Optional[str], Field(None, description="Имя для сортировки")]
    artistNationality: Annotated[Optional[str], Field(None, description="Национальность автора")]
    artistBeginDate: Annotated[Optional[str], Field(None, description="Год рождения автора")]
    artistEndDate: Annotated[Optional[str], Field(None, description="Год смерти автора")]
    artistGender: Annotated[Optional[str], Field(None, description="Пол автора")]
    artistWikidata_URL: Annotated[Optional[str], Field(None, description="URL в Wikidata")]
    artistULAN_URL: Annotated[Optional[str], Field(None, description="URL в ULAN")]

    # Даты создания
    objectDate: Annotated[Optional[str], Field(None, description="Дата создания")]
    objectBeginDate: Annotated[Optional[int], Field(None, description="Год начала создания")]
    objectEndDate: Annotated[Optional[int], Field(None, description="Год окончания создания")]

    # Физические характеристики
    medium: Annotated[Optional[str], Field(None, description="Материалы")]
    dimensions: Annotated[Optional[str], Field(None, description="Размеры")]

    # Права и кредиты
    creditLine: Annotated[Optional[str], Field(None, description="Кредитная строка")]
    rightsAndReproduction: Annotated[Optional[str], Field(None, description="Авторские права")]

    # Географические данные
    geographyType: Annotated[Optional[str], Field(None, description="Тип географической привязки")]
    city: Annotated[Optional[str], Field(None, description="Город создания")]
    state: Annotated[Optional[str], Field(None, description="Штат создания")]
    county: Annotated[Optional[str], Field(None, description="Округ создания")]
    country: Annotated[Optional[str], Field(None, description="Страна создания")]
    region: Annotated[Optional[str], Field(None, description="Регион создания")]
    subregion: Annotated[Optional[str], Field(None, description="Субрегион")]
    locale: Annotated[Optional[str], Field(None, description="Локация")]
    locus: Annotated[Optional[str], Field(None, description="Местонахождение")]
    excavation: Annotated[Optional[str], Field(None, description="Раскопки")]
    river: Annotated[Optional[str], Field(None, description="Река")]

    # Дополнительные метаданные
    classification: Annotated[Optional[str], Field(None, description="Классификация")]
    linkResource: Annotated[Optional[str], Field(None, description="URL страницы объекта")]
    metadataDate: Annotated[Optional[datetime], Field(None, description="Дата обновления метаданных")]
    repository: Annotated[Optional[str], Field(None, description="Репозиторий хранения")]
    objectURL: Annotated[Optional[str], Field(None, description="URL объекта")]
    objectWikidata_URL: Annotated[Optional[str], Field(None, description="URL в Wikidata")]
    isTimelineWork: Annotated[Optional[bool], Field(None, description="Флаг временной шкалы")]
    GalleryNumber: Annotated[Optional[str], Field(None, description="Номер галереи")]

    # Валидаторы

    @field_validator("primaryImage", "primaryImageSmall", mode="after")
    @classmethod
    def validate_url_fields(cls, v: Optional[str]) -> Optional[str]:
        """Проверяет корректность URL основных изображений."""
        if v and v.strip() and not v.startswith(("http://", "https://")):
            raise ValueError(f"URL должен начинаться с http:// или https://")
        return v

    @field_validator("artistWikidata_URL", "artistULAN_URL", "linkResource",
                     "objectURL", "objectWikidata_URL", mode="after")
    @classmethod
    def validate_optional_url_fields(cls, v: Optional[str]) -> Optional[str]:
        """Проверяет корректность опциональных URL полей."""
        if v and v.strip():
            if not v.startswith(("http://", "https://")):
                raise ValueError(f"URL должен начинаться с http:// или https://")
        return v

    @field_validator("additionalImages", mode="after")
    @classmethod
    def validate_additional_images_urls(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Проверяет корректность URL дополнительных изображений."""
        if v:
            for url in v:
                if url and not url.startswith(("http://", "https://")):
                    raise ValueError(f"URL должен начинаться с http:// или https://")
        return v

    @field_validator("additionalImages", "constituents", "measurements",
                     "dimensionsParsed", "tags", mode="before")
    @classmethod
    def validate_array_fields(cls, v: Any) -> Any:
        """Проверяет и нормализует поля-массивы."""
        if v is None:
            return []
        if not isinstance(v, list):
            raise TypeError(f"Поле должно быть списком")
        return v

    @field_validator("objectEndDate", mode="after")
    @classmethod
    def validate_end_date_after_start(cls, v: Optional[int], info) -> Optional[int]:
        """Проверяет, что дата окончания не раньше даты начала."""
        if v is not None:
            begin_date = info.data.get('objectBeginDate')
            if begin_date is not None and v < begin_date:
                raise ValueError(f"Дата окончания не может быть раньше даты начала")
        return v

    @field_validator("accessionYear", mode="after")
    @classmethod
    def validate_accession_year(cls, v: Optional[str]) -> Optional[str]:
        """Проверяет формат года приобретения."""
        if v and v.strip():
            if not re.search(r'\d{4}', v):
                raise ValueError(f"Год должен содержать 4 цифры")
        return v