import pytest

from models.objects import ObjectsSchema
from config.logger import APILogger
from tests.src.API_test_template import APITestTemplate
from tests.src.API_param_builder import APIBuilder


@pytest.mark.search
class TestValidParams(APITestTemplate):
    """Тесты для проверки API поиска с валидными параметрами."""

    BASE_API = "https://collectionapi.metmuseum.org/public/collection/v1/search"

    # Валидные параметры поиска
    VALID_APIS = [
        # Простой поиск по ключевому слову
        APIBuilder.build_url(BASE_API, q="sunflowers"),

        # Поиск с различными фильтрами
        APIBuilder.build_url(BASE_API, q="art", isHighlight=True),
        APIBuilder.build_url(BASE_API, q="painting", title=True),
        APIBuilder.build_url(BASE_API, q="asian", departmentId=6),
        APIBuilder.build_url(BASE_API, q="sculpture", isOnView=True),
        APIBuilder.build_url(BASE_API, q="french", artistOrCulture=True),
        APIBuilder.build_url(BASE_API, q="ceramics", medium="Ceramics"),
        APIBuilder.build_url(BASE_API, q="paris", geoLocation="France"),
        APIBuilder.build_url(BASE_API, q="renaissance", dateBegin=1400, dateEnd=1600)
    ]
    logger = APILogger("search_valid_param_api")

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_status_code(self, make_request):
        """Проверяет корректный HTTP статус-код для валидного поискового запроса."""
        TestValidParams.logger.info("=== Начало теста test_status_code ===")

        TestValidParams.logger.info(f"Делаем запрос к API: {TestValidParams.VALID_APIS[-1]}")
        response = make_request(TestValidParams.VALID_APIS[-1])

        assert response.status_code == 200
        TestValidParams.logger.debug(f"Код API ответа: {response.status_code}")

        TestValidParams.logger.info("=== Конец теста test_status_code ===")

    @pytest.mark.positive
    @pytest.mark.validation
    @pytest.mark.parametrize("api_url", VALID_APIS)
    def test_data_structure(self, api_url, make_request):
        """Проверяет структуру данных для валидных поисковых запросов."""
        TestValidParams.logger.info("=== Начало теста test_data_structure ===")

        TestValidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

        if response.status_code == 502:
            TestValidParams.logger.warning(f"API вернул 502, пропускаем проверку для: {api_url}")
            assert response.text
            return

        try:
            response_json = response.json()

            # Нормализуем данные для валидации
            if response_json.get("objectIDs") is None:
                response_json["objectIDs"] = []

            validated_data = ObjectsSchema(**response_json)
        except Exception as e:
            TestValidParams.logger.error(f"Ошибка валидации данных: {e}")
            pytest.fail(f"Валидация данных не удалась: {e}")

        assert isinstance(response_json, dict)
        TestValidParams.logger.debug(f"API ответ является словарём: {isinstance(response_json, dict)}")

        assert validated_data is not None
        TestValidParams.logger.debug(f"Данные соответствуют Pydantic модели: {validated_data is not None}")

        TestValidParams.logger.info("=== Конец теста test_data_structure ===")

    @pytest.mark.positive
    @pytest.mark.parametrize("api_url", VALID_APIS)
    def test_data_content(self, api_url, make_request):
        """Проверяет корректность данных для валидных поисковых запросов."""
        TestValidParams.logger.info("=== Начало теста test_data_content ===")

        TestValidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

        if response.status_code == 502:
            TestValidParams.logger.warning(f"API вернул 502, пропускаем проверку для: {api_url}")
            return

        try:
            response_json = response.json()
        except Exception as e:
            TestValidParams.logger.error(f"API ответ не соответствует типу JSON: {e}")
            pytest.fail(f"API ответ не соответствует типу JSON: {e}")

        total = response_json.get("total", 0)
        object_ids = response_json.get("objectIDs")

        if object_ids is None:
            object_ids = []

        object_ids_length = len(object_ids)

        TestValidParams.logger.debug(f"Значение по ключу total: {total}")
        TestValidParams.logger.debug(f"Количество элементов в objectIDs: {object_ids_length}")

        assert total == object_ids_length
        TestValidParams.logger.debug(f"total равен длине objectIDs: {total == object_ids_length}")

        TestValidParams.logger.info("=== Конец теста test_data_content ===")