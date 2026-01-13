import pytest

from models.object import ObjectSchema
from config.logger import APILogger
from tests.src.API_test_template import APITestTemplate
from tests.src.API_param_builder import APIBuilder


@pytest.mark.object
class TestValidParams(APITestTemplate):

    BASE_API = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

    VALID_APIS = [
        (APIBuilder.build_url_with_id(BASE_API, 437133)),
        (APIBuilder.build_url_with_id(BASE_API, 45734))
    ]
    logger = APILogger("object_valid_param_api")

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_status_code(self, make_request):
        TestValidParams.logger.info("=== Начало теста test_status_code ===")

        TestValidParams.logger.info(f"Делаем запрос к API: {TestValidParams.VALID_APIS[0]}")
        response = make_request(TestValidParams.VALID_APIS[0])

        assert response.status_code == 200
        TestValidParams.logger.debug(f"Код API ответа: {response.status_code}")

        TestValidParams.logger.info("=== Конец теста test_status_code ===")

    @pytest.mark.positive
    @pytest.mark.validation
    @pytest.mark.parametrize("api_url", VALID_APIS)
    def test_data_structure(self, api_url, make_request):
        TestValidParams.logger.info("=== Начало теста test_data_structure ===")

        TestValidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

        try:
            response_json = response.json()
            validated_data = ObjectSchema(**response_json)
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
        TestValidParams.logger.info("=== Начало теста test_data_content ===")

        TestValidParams.logger.info(f"Делаем запрос к API: {api_url}")
        response = make_request(api_url)

        try:
            response_json = response.json()
        except Exception as e:
            TestValidParams.logger.error(f"API ответ не соответствует типу JSON: {e}")
            pytest.fail(f"API ответ не соответствует типу JSON: {e}")

        assert response_json
        TestValidParams.logger.debug(f"API ответ не пуст {response_json != {}}")

