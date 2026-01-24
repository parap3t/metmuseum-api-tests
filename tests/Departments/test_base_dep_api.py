import pytest

from config.logger import APILogger
from tests.src.API_test_template import APITestTemplate
from models.departments import DepartmentsSchema


@pytest.mark.departments
class TestBaseAPI(APITestTemplate):
    """Тесты для API департаментов."""

    API_URL = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
    logger = APILogger("departments_base_api")

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_status_code(self, make_request):
        """Проверяет корректный HTTP статус-код ответа API."""
        TestBaseAPI.logger.info("=== Начало теста test_status_code ===")

        response = make_request(TestBaseAPI.API_URL)

        assert response.status_code == 200, "API должен возвращать статус 200"
        TestBaseAPI.logger.debug(f"Код API ответа: {response.status_code}")

        TestBaseAPI.logger.info("=== Конец теста test_status_code ===")

    @pytest.mark.validation
    @pytest.mark.positive
    def test_data_structure(self, make_request):
        """Проверяет структуру данных в ответе API."""
        TestBaseAPI.logger.info("=== Начало теста test_data_structure ===")

        response = make_request(TestBaseAPI.API_URL)

        try:
            response_json = response.json()
            validated_data = DepartmentsSchema(**response_json)

        except Exception as e:
            TestBaseAPI.logger.error(f"Ошибка валидации данных: {e}")
            pytest.fail(f"Валидация данных не удалась: {e}")

        assert isinstance(response_json, dict), "Ответ API должен быть словарём"
        TestBaseAPI.logger.debug(f"API ответ является словарём: {isinstance(response_json, dict)}")

        assert validated_data is not None, "Данные должны соответствовать схеме DepartmentsSchema"
        TestBaseAPI.logger.debug(f"Данные соответствуют Pydantic модели: {validated_data is not None}")

        TestBaseAPI.logger.info("=== Конец теста test_data_structure ===")

    @pytest.mark.positive
    def test_data_content(self, make_request):
        """Проверяет наличие данных в ответе API."""
        TestBaseAPI.logger.info("=== Начало теста test_data_content ===")

        response = make_request(TestBaseAPI.API_URL)

        try:
            response_json = response.json()
        except Exception as e:
            TestBaseAPI.logger.error(f"API ответ не соответствует типу JSON: {e}")
            pytest.fail(f"API ответ не соответствует типу JSON: {e}")

        departments = response_json.get("departments", [])

        assert len(departments) > 0, "API должен возвращать непустой список департаментов"
        TestBaseAPI.logger.debug(f"Количество отделов > 0: {len(departments) > 0}")

        TestBaseAPI.logger.info("=== Конец теста test_data_content ===")