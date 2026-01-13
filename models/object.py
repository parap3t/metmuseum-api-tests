from datetime import datetime
from typing import List, Dict, Any, Optional, Annotated
from pydantic import BaseModel, Field, field_validator, ConfigDict


class ObjectSchema(BaseModel):
    model_config = ConfigDict(extra='ignore')

    objectID: Annotated[int, Field(ge=0, description="Уникальный идентификационный номер объекта")]

    isHighlight: Annotated[Optional[bool], Field(None, description="Флаг популярного и важного объекта коллекции")]
    accessionNumber: Annotated[Optional[str], Field(None, description="Номер поступления объекта (не всегда уникальный)")]
    accessionYear: Annotated[Optional[str], Field(None, description="Год приобретения объекта музеем")]
    isPublicDomain: Annotated[Optional[bool], Field(None, description="Флаг нахождения объекта в общественном достоянии")]
    primaryImage: Annotated[Optional[str], Field(None, description="URL основного изображения объекта в формате JPEG")]
    primaryImageSmall: Annotated[Optional[str], Field(None, description="URL уменьшенного изображения объекта в формате JPEG")]

    additionalImages: Annotated[Optional[List[str]], Field(default=[], description="Массив URL дополнительных изображений объекта")]
    constituents: Annotated[Optional[List[Dict[str, Any]]], Field(default=[], description="Массив связанных лиц с их ролями и данными")]
    measurements: Annotated[Optional[List[Dict[str, Any]]], Field(default=[], description="Массив измерений объекта с описаниями")]
    dimensionsParsed: Annotated[Optional[List[Dict[str, Any]]], Field(default=[], description="Размеры объекта в сантиметрах, распарсенные")]
    tags: Annotated[Optional[List[Dict[str, Any]]], Field(default=[], description="Массив тегов предмета с URL словарей")]

    department: Annotated[Optional[str], Field(None, description="Кураторский отдел музея, ответственный за объект")]
    objectName: Annotated[Optional[str], Field(None, description="Физический тип объекта (картина, скульптура и т.д.)")]
    title: Annotated[Optional[str], Field(None, description="Название или заголовок произведения искусства")]
    culture: Annotated[Optional[str], Field(None, description="Культура или народность, создавшая объект")]
    period: Annotated[Optional[str], Field(None, description="Временной период создания объекта")]
    dynasty: Annotated[Optional[str], Field(None, description="Правящая династия на момент создания")]
    reign: Annotated[Optional[str], Field(None, description="Правление монарха на момент создания")]
    portfolio: Annotated[Optional[str], Field(None, description="Серия или группа, к которой относится объект")]

    artistRole: Annotated[Optional[str], Field(None, description="Роль автора в создании объекта")]
    artistPrefix: Annotated[Optional[str], Field(None, description="Квалификатор авторства (например, 'в стиле')")]
    artistDisplayName: Annotated[Optional[str], Field(None, description="Имя автора для отображения")]
    artistDisplayBio: Annotated[Optional[str], Field(None, description="Биография автора с национальностью и годами жизни")]
    artistSuffix: Annotated[Optional[str], Field(None, description="Дополнительная информация о роли автора")]
    artistAlphaSort: Annotated[Optional[str], Field(None, description="Имя автора для сортировки по алфавиту")]
    artistNationality: Annotated[Optional[str], Field(None, description="Национальность или происхождение автора")]
    artistBeginDate: Annotated[Optional[str], Field(None, description="Год рождения автора")]
    artistEndDate: Annotated[Optional[str], Field(None, description="Год смерти автора")]
    artistGender: Annotated[Optional[str], Field(None, description="Пол автора")]
    artistWikidata_URL: Annotated[Optional[str], Field(None, description="URL страницы автора в Wikidata")]
    artistULAN_URL: Annotated[Optional[str], Field(None, description="URL страницы автора в ULAN")]

    objectDate: Annotated[Optional[str], Field(None, description="Дата создания в строковом формате")]
    objectBeginDate: Annotated[Optional[int], Field(None, description="Год начала создания в числовом формате")]
    objectEndDate: Annotated[Optional[int], Field(None, description="Год окончания создания в числовом формате")]

    medium: Annotated[Optional[str], Field(None, description="Материалы, использованные при создании")]
    dimensions: Annotated[Optional[str], Field(None, description="Размеры объекта в текстовом формате")]

    creditLine: Annotated[Optional[str], Field(None, description="Кредитная строка с указанием происхождения")]
    rightsAndReproduction: Annotated[Optional[str], Field(None, description="Информация об авторских правах")]

    geographyType: Annotated[Optional[str], Field(None, description="Тип географической привязки")]
    city: Annotated[Optional[str], Field(None, description="Город создания")]
    state: Annotated[Optional[str], Field(None, description="Штат/провинция создания")]
    county: Annotated[Optional[str], Field(None, description="Округ создания")]
    country: Annotated[Optional[str], Field(None, description="Страна создания")]
    region: Annotated[Optional[str], Field(None, description="Регион (более конкретно, чем страна)")]
    subregion: Annotated[Optional[str], Field(None, description="Субрегион (более конкретно, чем регион)")]
    locale: Annotated[Optional[str], Field(None, description="Локация (более конкретно, чем субрегион)")]
    locus: Annotated[Optional[str], Field(None, description="Местонахождение (более конкретно, чем локация)")]
    excavation: Annotated[Optional[str], Field(None, description="Название раскопок")]
    river: Annotated[Optional[str], Field(None, description="Река, связанная с объектом")]

    classification: Annotated[Optional[str], Field(None, description="Классификационный тип объекта")]
    linkResource: Annotated[Optional[str], Field(None, description="URL страницы объекта на сайте музея")]
    metadataDate: Annotated[Optional[datetime], Field(None, description="Дата последнего обновления метаданных")]
    repository: Annotated[Optional[str], Field(None, description="Репозиторий хранения объекта")]
    objectURL: Annotated[Optional[str], Field(None, description="URL объекта на сайте музея")]
    objectWikidata_URL: Annotated[Optional[str], Field(None, description="URL страницы объекта в Wikidata")]
    isTimelineWork: Annotated[Optional[bool], Field(None, description="Флаг нахождения объекта на временной шкале истории искусства")]
    GalleryNumber: Annotated[Optional[str], Field(None, description="Номер галереи, где выставлен объект")]

    @field_validator("primaryImage", "primaryImageSmall", mode="after")
    @classmethod
    def validate_url_fields(cls, v: Optional[str]) -> Optional[str]:
        if v and v.strip() and not v.startswith(("http://", "https://")):
            raise ValueError(
                f"URL должен начинаться с http:// или https://, получено: {v[:50]}{'...' if len(v) > 50 else ''}")
        return v

    @field_validator("artistWikidata_URL", "artistULAN_URL", "linkResource",
                     "objectURL", "objectWikidata_URL", mode="after")
    @classmethod
    def validate_optional_url_fields(cls, v: Optional[str]) -> Optional[str]:
        if v and v.strip():
            if not v.startswith(("http://", "https://")):
                raise ValueError(
                    f"URL должен начинаться с http:// или https://, получено: {v[:50]}{'...' if len(v) > 50 else ''}")
        return v

    @field_validator("additionalImages", mode="after")
    @classmethod
    def validate_additional_images_urls(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        if v:
            for i, url in enumerate(v):
                if url and not url.startswith(("http://", "https://")):
                    raise ValueError(
                        f"additionalImages[{i}] должен начинаться с http:// или https://, "
                        f"получено: {url[:50]}{'...' if len(url) > 50 else ''}"
                    )
        return v

    @field_validator("additionalImages", "constituents", "measurements", "dimensionsParsed", "tags", mode="before")
    @classmethod
    def validate_array_fields(cls, v: Any) -> Any:
        if v is None:
            return []
        if not isinstance(v, list):
            raise TypeError(f"Поле должно быть list, получен {type(v).__name__}: {v}")
        return v

    @field_validator("objectEndDate", mode="after")
    @classmethod
    def validate_end_date_after_start(cls, v: Optional[int], info) -> Optional[int]:
        if v is not None:
            begin_date = info.data.get('objectBeginDate')
            if begin_date is not None and v < begin_date:
                raise ValueError(
                    f"objectEndDate ({v}) не может быть раньше objectBeginDate ({begin_date})"
                )
        return v

    @field_validator("accessionYear", mode="after")
    @classmethod
    def validate_accession_year(cls, v: Optional[str]) -> Optional[str]:
        if v and v.strip():
            import re
            if not re.search(r'\d{4}', v):
                raise ValueError(f"accessionYear должен содержать год (4 цифры), получено: {v}")
        return v

    @field_validator("objectID", mode="after")
    @classmethod
    def validate_object_id(cls, v: int) -> int:
        if v <= 0:
            raise ValueError(f"objectID должен быть положительным числом, получено: {v}")
        return v