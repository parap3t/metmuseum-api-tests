import pytest

from models.objects import ObjectsSchema
from config.logger import APILogger
from tests.src.API_test_template import APITestTemplate
from tests.src.API_param_builder import APIBuilder


@pytest.mark.objects
class TestValidParams(APITestTemplate):
    """Тесты для проверки API объектов с валидными query-параметрами."""

    BASE_API = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

    # Валидные URL с query-параметрами
    VALID_APIS = [
        APIBuilder.build_url(BASE_API, departmentIds="1"),
        APIBuilder.build_url(BASE_API, metadataDate="2018-10-22", departmentIds="3|9|12"),
        APIBuilder.build_url(BASE_API, metadataDate="2018-10-22"),
    ]
    logger = APILogger("objects_valid_param_api")

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_status_code(self, make_request):
        """Проверяет корректный HTTP статус-код для валидного запроса с параметрами."""
        TestValidParams.logger.info("=== Начало теста test_status_code ===")

        TestValidParams.logger.info(f"Делаем запрос к API: {TestValidParams.VALID_APIS[1]}")
        response = make_request(TestValidParams.VALID_APIS[1])

        assert response.status_code == 200
        TestValidParams.logger.debug(f"Код API ответа: {response.status_code}")

        TestValidParams.logger.info("=== Конец теста test_status_code ===")

    @pytest.mark.positive
    @pytest.mark.validation
    @pytest.mark.parametrize("api_url", VALID_APIS)
    def test_data_structure(self, api_url, make_request):
        """Проверяет структуру данных для валидных запросов с параметрами."""
        TestValidParams.logger.info("=== Начало теста test_data_structure ===")

        TestValidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

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
        """Проверяет корректность данных для валидных запросов с параметрами."""
        TestValidParams.logger.info("=== Начало теста test_data_content ===")

        TestValidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

        try:
            response_json = response.json()
        except Exception as e:
            TestValidParams.logger.error(f"API ответ не соответствует типу JSON: {e}")
            pytest.fail(f"API ответ не соответствует типу JSON: {e}")

        total = response_json.get("total")
        object_ids = response_json.get("objectIDs")

        # Нормализуем объект для проверок
        if object_ids is None:
            object_ids = []

        object_ids_length = len(object_ids)

        assert total > 0
        TestValidParams.logger.debug(f"Значение по ключу total: {total}")

        assert object_ids_length > 0
        TestValidParams.logger.debug(f"Количество элементов в objectIDs: {object_ids_length}")

        assert total == object_ids_length
        TestValidParams.logger.debug(
            f"Количество элементов в objectIDs равно значению total: {total == object_ids_length}")

        TestValidParams.logger.info("=== Конец теста test_data_content ===")