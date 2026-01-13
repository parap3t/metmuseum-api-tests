import pytest

from models.objects import ObjectsSchema
from config.logger import APILogger
from tests.src.API_test_template import APITestTemplate

@pytest.mark.search
class TestBaseAPI(APITestTemplate):
    API_URL = "https://collectionapi.metmuseum.org/public/collection/v1/search?q="
    logger = APILogger("search_base_api")

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_status_code(self, make_request):
        TestBaseAPI.logger.info("=== Начало теста test_status_code ===")

        response = make_request(TestBaseAPI.API_URL)

        assert response.status_code == 200
        TestBaseAPI.logger.debug(f"Код API ответа: {response.status_code}")

        TestBaseAPI.logger.info("=== Конец теста test_status_code ===")

    @pytest.mark.positive
    @pytest.mark.validation
    def test_data_structure(self, make_request):
        TestBaseAPI.logger.info("=== Начало теста test_data_structure ===")

        response = make_request(TestBaseAPI.API_URL)

        try:
            response_json = response.json()

            if response_json.get("objectIDs") is None:
                response_json["objectIDs"] = []

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
        TestBaseAPI.logger.info("=== Начало теста test_data_content ===")

        response = make_request(TestBaseAPI.API_URL)

        try:
            response_json = response.json()
        except Exception as e:
            TestBaseAPI.logger.error(f"API ответ не соответствует типу JSON: {e}")
            pytest.fail(f"API ответ не соответствует типу JSON: {e}")

        total = response_json.get("total", 0)
        object_ids = response_json.get("objectIDs")

        if object_ids is None:
            object_ids = []

        object_ids_length = len(object_ids)

        assert total == 0
        TestBaseAPI.logger.debug(f"Значение по ключу total: {total} (ожидалось: 0)")

        assert object_ids_length == 0
        TestBaseAPI.logger.debug(f"Количество элементов в objectIDs: {object_ids_length} (ожидалось: 0)")

        assert total == object_ids_length
        TestBaseAPI.logger.debug(f"Количество элементов в objectIDs равно значению total: {total == object_ids_length}")

        TestBaseAPI.logger.info("=== Конец теста test_data_content ===")