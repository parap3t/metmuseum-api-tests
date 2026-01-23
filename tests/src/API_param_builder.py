from typing import Optional


class APIBuilder:
    """Класс для формирования URL адресов API запросов."""

    @staticmethod
    def build_url(endpoint: str, sep: Optional[str] = "?", **params) -> str:
        """
        Формирует URL с query-параметрами.

        Args:
            endpoint: Базовый URL endpoint
            sep: Разделитель перед query-параметрами
            **params: Параметры для добавления в query string
        """
        url = f"{endpoint}"

        if params:
            # Фильтруем None значения
            filtered_params = {k: v for k, v in params.items() if v is not None}
            query_string = "&".join(f"{k}={v}" for k, v in filtered_params.items())
            url += f"{sep}{query_string}"

        return url

    @staticmethod
    def build_url_with_id(base_url: str, object_id: str) -> str:
        """
        Формирует URL для получения объекта по ID.

        Args:
            base_url: Базовый URL endpoint
            object_id: Идентификатор объекта
        """
        url = f"{base_url}/{object_id}"

        return url