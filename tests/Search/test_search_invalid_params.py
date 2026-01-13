import pytest

from config.logger import APILogger
from tests.src.API_test_template import APITestTemplate
from tests.src.API_param_builder import APIBuilder


@pytest.mark.search
class TestInvalidParams(APITestTemplate):
    BASE_API = "https://collectionapi.metmuseum.org/public/collection/v1/search"

    INVALID_APIS = [

        APIBuilder.build_url(BASE_API, isHighlight=True),
        APIBuilder.build_url(BASE_API, title=True),
        APIBuilder.build_url(BASE_API, departmentId=1),

        APIBuilder.build_url(BASE_API, q="test", isHighlight=123),
        APIBuilder.build_url(BASE_API, q="test", departmentId=-1),
        APIBuilder.build_url(BASE_API, q="test", geoLocation=123),

        APIBuilder.build_url(BASE_API, q="test", dateBegin="abc", dateEnd="def"),
        APIBuilder.build_url(BASE_API, q="test", dateBegin=999999, dateEnd=-999999),

        APIBuilder.build_url(BASE_API, q="null"),
        APIBuilder.build_url(BASE_API, q="undefined"),
        APIBuilder.build_url(BASE_API, q=""),
    ]

    logger = APILogger("search_invalid_param_api")

    @pytest.mark.negative
    @pytest.mark.parametrize("api_url", INVALID_APIS)
    def test_status_code(self, api_url, make_request):
        TestInvalidParams.logger.info("=== Начало теста test_status_code ===")

        TestInvalidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

        assert response.status_code in [200, 400, 422, 502]

        TestInvalidParams.logger.debug(f"Код API ответа: {response.status_code}")

        TestInvalidParams.logger.info("=== Конец теста test_status_code ===")

    @pytest.mark.negative
    @pytest.mark.parametrize("api_url", INVALID_APIS)
    def test_data_structure(self, api_url, make_request):
        TestInvalidParams.logger.info("=== Начало теста test_data_structure ===")

        TestInvalidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

        if response.status_code == 502:
            TestInvalidParams.logger.warning(f"API вернул 502 для: {api_url}")
            assert response.text
            return

        if response.status_code in [400, 422]:
            try:
                response_json = response.json()
                TestInvalidParams.logger.debug(f"API вернул JSON для ошибки: {response_json}")
            except:
                assert response.text
                TestInvalidParams.logger.debug(f"API вернул текст для ошибки: {response.text[:100]}...")
            return

        try:
            response_json = response.json()
            assert isinstance(response_json, dict)
            TestInvalidParams.logger.debug(f"API ответ является словарём: {isinstance(response_json, dict)}")
        except Exception as e:
            TestInvalidParams.logger.error(f"API ответ не соответствует типу JSON: {e}")
            pytest.fail(f"API ответ не соответствует типу JSON: {e}")

        TestInvalidParams.logger.info("=== Конец теста test_data_structure ===")

    @pytest.mark.negative
    @pytest.mark.parametrize("api_url", INVALID_APIS)
    def test_data_content(self, api_url, make_request):
        TestInvalidParams.logger.info("=== Начало теста test_data_content ===")

        TestInvalidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

        if response.status_code in [400, 422, 502]:
            TestInvalidParams.logger.warning(
                f"Пропускаем проверку контента для статуса {response.status_code}: {api_url}")
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

        object_ids_length = len(object_ids)

        TestInvalidParams.logger.debug(f"API вернул: total={total}, objectIDs length={object_ids_length}")

        assert total == object_ids_length
        TestInvalidParams.logger.debug(
            f"Количество элементов в objectIDs равно значению total: {total == object_ids_length}")

        TestInvalidParams.logger.info("=== Конец теста test_data_content ===")