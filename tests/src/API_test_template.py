import requests
import pytest

from requests.exceptions import RequestException, Timeout
from abc import ABC, abstractmethod

class APITestTemplate(ABC):

    @pytest.fixture(scope="class")
    def make_request(self):
        def _make_request(api_url, timeout=10):
            try:
                response = requests.get(api_url, timeout=timeout)
                return response
            except Timeout:
                pytest.fail(f"API не отвечает {timeout}сек. Сервис перегружен или умер")
            except RequestException as e:
                pytest.skip(f"API недоступно: {e}")

        return _make_request

    @abstractmethod
    def test_status_code(self):
        pass

    @abstractmethod
    def test_data_structure(self):
        pass

    @abstractmethod
    def test_data_content(self):
        pass