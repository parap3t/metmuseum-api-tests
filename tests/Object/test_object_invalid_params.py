import pytest

from config.logger import APILogger
from tests.src.API_test_template import APITestTemplate
from tests.src.API_param_builder import APIBuilder


@pytest.mark.object
class TestInvalidParams(APITestTemplate):
    """Тесты для проверки API объектов с невалидными параметрами."""

    BASE_API = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

    # Невалидные URL для тестирования негативных сценариев
    INVALID_APIS = [
        (APIBuilder.build_url_with_id(BASE_API, "")),  # Пустой ID
        (APIBuilder.build_url_with_id(BASE_API, "-10000000")),  # Отрицательный ID
        (APIBuilder.build_url_with_id(BASE_API, "999999999")),  # Несуществующий ID
        (APIBuilder.build_url_with_id(BASE_API, "absbsbs"))  # Некорректный формат ID
    ]

    logger = APILogger("object_invalid_param_api")

    @pytest.mark.negative
    @pytest.mark.parametrize("api_url", INVALID_APIS)
    def test_status_code(self, api_url, make_request):
        """Проверяет корректные статус-коды для невалидных запросов."""
        TestInvalidParams.logger.info("=== Начало теста test_status_code ===")

        TestInvalidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

        assert response.status_code in [400, 404, 422], "Для невалидных запросов ожидаются коды 400, 404 или 422"
        TestInvalidParams.logger.debug(f"Код API ответа: {response.status_code}")

        TestInvalidParams.logger.info("=== Конец теста test_status_code ===")

    @pytest.mark.negative
    @pytest.mark.parametrize("api_url", INVALID_APIS)
    def test_data_structure(self, api_url, make_request):
        """Проверяет структуру данных при невалидных запросах."""
        TestInvalidParams.logger.info("=== Начало теста test_data_structure ===")

        TestInvalidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

        try:
            response_json = response.json()
        except Exception as e:
            TestInvalidParams.logger.error(f"API ответ не соответствует типу JSON: {e}")
            pytest.fail(f"API ответ не соответствует типу JSON: {e}")

        assert isinstance(response_json, dict), "Ответ API должен быть словарём"
        TestInvalidParams.logger.debug(f"API ответ является словарём: {isinstance(response_json, dict)}")

        TestInvalidParams.logger.info("=== Конец теста test_data_structure ===")

    @pytest.mark.negative
    @pytest.mark.parametrize("api_url", INVALID_APIS)
    def test_data_content(self, api_url, make_request):
        """Проверяет наличие данных в ответе на невалидные запросы."""
        TestInvalidParams.logger.info("=== Начало теста test_data_content ===")

        TestInvalidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

        try:
            response_json = response.json()
        except Exception as e:
            TestInvalidParams.logger.error(f"API ответ не соответствует типу JSON: {e}")
            pytest.fail(f"API ответ не соответствует типу JSON: {e}")

        assert response_json, "Ответ должен содержать данные (не быть пустым)"
        TestInvalidParams.logger.debug(f"API ответ не пуст {response_json != {} }")

        TestInvalidParams.logger.info("=== Конец теста test_data_content ===")