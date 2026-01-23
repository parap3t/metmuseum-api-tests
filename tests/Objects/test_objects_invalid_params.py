import pytest

from config.logger import APILogger
from tests.src.API_test_template import APITestTemplate
from tests.src.API_param_builder import APIBuilder


@pytest.mark.objects
class TestInvalidParams(APITestTemplate):
    """Тесты для проверки API объектов с невалидными query-параметрами."""

    BASE_API = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

    # Невалидные URL с ожидаемыми статус-кодами
    INVALID_APIS = [
        # Невалидные значения departmentIds
        (APIBuilder.build_url(BASE_API, departmentIds="abc"), 502),
        (APIBuilder.build_url(BASE_API, departmentIds=-999999), 200),
        (APIBuilder.build_url(BASE_API, departmentIds=999999999), 200),

        # Невалидные значения metadataDate
        (APIBuilder.build_url(BASE_API, metadataDate="2023-13-01"), 400),
        (APIBuilder.build_url(BASE_API, metadataDate="2023-02-30"), 400),
        (APIBuilder.build_url(BASE_API, metadataDate="01-01-2023"), 400),
        (APIBuilder.build_url(BASE_API, metadataDate="2023/01/01"), 400),
        (APIBuilder.build_url(BASE_API, metadataDate="1800-00-00"), 400),

        # Комбинированные невалидные параметры
        (APIBuilder.build_url(BASE_API, departmentIds="abc", metadataDate="invalid"), 400)
    ]

    logger = APILogger("objects_invalid_param_api")

    @pytest.mark.negative
    @pytest.mark.parametrize("api_url, expected_status", INVALID_APIS)
    def test_status_code(self, api_url, expected_status, make_request):
        """Проверяет ожидаемые статус-коды для невалидных параметров."""
        TestInvalidParams.logger.info("=== Начало теста test_status_code ===")

        TestInvalidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

        assert response.status_code == expected_status
        TestInvalidParams.logger.debug(f"Код API ответа: {response.status_code} (ожидался: {expected_status})")

        TestInvalidParams.logger.info("=== Конец теста test_status_code ===")

    @pytest.mark.negative
    @pytest.mark.parametrize("api_url,expected_status", INVALID_APIS)
    def test_data_structure(self, api_url, expected_status, make_request):
        """Проверяет структуру данных при невалидных параметрах."""
        TestInvalidParams.logger.info("=== Начало теста test_data_structure ===")

        TestInvalidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

        if expected_status == 502:
            TestInvalidParams.logger.warning(f"API вернул {expected_status} Bad Gateway")
            assert response.text
            TestInvalidParams.logger.debug(f"Текст ответа: {response.text[:100]}...")

        elif expected_status == 400:
            try:
                response_json = response.json()
                TestInvalidParams.logger.debug(f"JSON ответ: {response_json}")
                assert isinstance(response_json, dict)
            except:
                assert response.text
                TestInvalidParams.logger.debug(f"Текстовый ответ: {response.text[:100]}...")

        else:
            try:
                response_json = response.json()
                assert isinstance(response_json, dict)
                TestInvalidParams.logger.debug(f"API ответ является словарём: {isinstance(response_json, dict)}")
            except Exception as e:
                TestInvalidParams.logger.error(f"API ответ не соответствует типу JSON: {e}")
                pytest.fail(f"API ответ не соответствует типу JSON: {e}")

        TestInvalidParams.logger.info("=== Конец теста test_data_structure ===")

    @pytest.mark.negative
    @pytest.mark.parametrize("api_url,expected_status", INVALID_APIS)
    def test_data_content(self, api_url, expected_status, make_request):
        """Проверяет содержимое данных при невалидных параметрах."""
        TestInvalidParams.logger.info("=== Начало теста test_data_content ===")

        TestInvalidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

        if expected_status in [502, 400]:
            TestInvalidParams.logger.warning(f"Пропускаем проверку для {expected_status} ошибки")
            assert response.text
            return

        try:
            response_json = response.json()
        except Exception as e:
            TestInvalidParams.logger.error(f"API ответ не соответствует типу JSON: {e}")
            pytest.fail(f"API ответ не соответствует типу JSON: {e}")

        total = response_json.get("total", 0)
        object_ids = response_json.get("objectIDs")

        if object_ids is None:
            object_ids = []

        TestInvalidParams.logger.debug(f"total={total}, objectIDs length={len(object_ids)}")

        assert total == len(object_ids)
        TestInvalidParams.logger.debug(f"total равен длине objects_ids: {total == len(object_ids)}")

        if "departmentIds=999999999" in api_url or "departmentIds=-999999" in api_url:
            assert total == 0

        TestInvalidParams.logger.info("=== Конец теста test_data_content ===")