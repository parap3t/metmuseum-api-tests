import requests
import pytest

from requests.exceptions import RequestException, Timeout
from abc import ABC, abstractmethod


class APITestTemplate(ABC):
    """
    Абстрактный базовый класс для тестирования REST API.

    Предоставляет:
    - Фикстуру make_request для выполнения HTTP-запросов
    - Абстрактные методы для обязательных проверок API
    """

    @pytest.fixture(scope="class")
    def make_request(self):
        """
        Фикстура для выполнения HTTP GET запросов.

        Args:
            api_url (str): URL API для запроса
            timeout (int): Таймаут в секундах (по умолчанию 10)

        Returns:
            requests.Response: Объект ответа от API

        Raises:
            pytest.fail: При таймауте - сервис не отвечает в заданное время
            pytest.skip: При других ошибках запроса
        """

        def _make_request(api_url, timeout=10):
            try:
                response = requests.get(api_url, timeout=timeout)
                return response
            except Timeout:
                # Таймаут - критическая ошибка
                pytest.fail(f"API не отвечает {timeout}сек.")
            except RequestException as e:
                # Другие ошибки подключения
                pytest.skip(f"API недоступно: {e}")

        return _make_request

    @abstractmethod
    def test_status_code(self):
        """Проверка HTTP статус-кода ответа API."""
        pass

    @abstractmethod
    def test_data_structure(self):
        """Проверка структуры данных в ответе API."""
        pass

    @abstractmethod
    def test_data_content(self):
        """Проверка содержимого данных в ответе API."""
        pass