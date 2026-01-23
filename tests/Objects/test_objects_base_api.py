import pytest

from models.objects import ObjectsSchema
from config.logger import APILogger
from tests.src.API_test_template import APITestTemplate


@pytest.mark.objects
class TestBaseAPI(APITestTemplate):
    """Тесты для базового API объектов музея."""

    API_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
    logger = APILogger("objects_base_api")

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_status_code(self, make_request):
        """Проверяет корректный HTTP статус-код ответа API объектов."""
        TestBaseAPI.logger.info("=== Начало теста test_status_code ===")

        response = make_request(TestBaseAPI.API_URL)

        assert response.status_code == 200
        TestBaseAPI.logger.debug(f"Код API ответа: {response.status_code}")

        TestBaseAPI.logger.info("=== Конец теста test_status_code ===")

    @pytest.mark.validation
    @pytest.mark.positive
    def test_data_structure(self, make_request):
        """Проверяет структуру данных в ответе API объектов."""
        TestBaseAPI.logger.info("=== Начало теста test_data_structure ===")

        response = make_request(TestBaseAPI.API_URL)

        try:
            response_json = response.json()
            validated_data = ObjectsSchema(**response_json)

        except Exception as e:
            TestBaseAPI.logger.error(f"Ошибка валидации данных: {e}")
            pytest.fail(f"Валидация данных не удалась: {e}")

        assert isinstance(response_json, dict)
        TestBaseAPI.logger.debug(f"API ответ является словарём: {isinstance(response_json, dict)}")

        assert validated_data is not None
        TestBaseAPI.logger.debug(f"Данные соответствуют Pydantic модели: {validated_data is not None}")

        TestBaseAPI.logger.info("=== Конец теста test_data_structure ===")

    @pytest.mark.positive
    def test_data_content(self, make_request):
        """Проверяет корректность данных в ответе API объектов."""
        TestBaseAPI.logger.info("=== Начало теста test_data_content ===")

        response = make_request(TestBaseAPI.API_URL)

        try:
            response_json = response.json()
        except Exception as e:
            TestBaseAPI.logger.error(f"API ответ не соответствует типу JSON: {e}")
            pytest.fail(f"API ответ не соответствует типу JSON: {e}")

        total = response_json.get("total", 0)
        object_ids = response_json.get("objectIDs", [])
        object_ids_length = len(object_ids)

        assert total > 0
        TestBaseAPI.logger.debug(f"Значение по ключу total > 0: {total > 0}")

        assert object_ids_length > 0
        TestBaseAPI.logger.debug(f"Количество элементов в objectIDs > 0: {object_ids_length > 0}")

        assert total == object_ids_length
        TestBaseAPI.logger.debug(f"Количество элементов в objectIDs равно значению total: {total == object_ids_length}")

        TestBaseAPI.logger.info("=== Конец теста test_data_content ===")