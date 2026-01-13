from typing import Optional

class APIBuilder:
    @staticmethod
    def build_url(endpoint: str, sep: Optional[str] = "?", **params) -> str:
        url = f"{endpoint}"

        if params:
            # Фильтруем None значения
            filtered_params = {k: v for k, v in params.items() if v is not None}
            query_string = "&".join(f"{k}={v}" for k, v in filtered_params.items())
            url += f"{sep}{query_string}"

        return url

    @staticmethod
    def build_url_with_id(base_url: str, object_id: str) -> str:
        """Строит URL с ID объекта"""
        url = f"{base_url}/{object_id}"

        return url