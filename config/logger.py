import logging
from pathlib import Path


class APILogger:
    """Простой логер для API тестов"""

    def __init__(self, api_name: str, log_dir: str = None):
        """
        Создает логер для конкретного API.

        Args:
            api_name: Имя API (departments_base_api, objects_base_api и т.д.)
            log_dir: Путь к директории логов. Если None, используется ../api_logs
        """
        self.api_name = api_name

        # Определяем путь к директории логов
        if log_dir is None:
            # Предполагаем, что скрипт в папке objects, а api_logs на уровень выше
            current_dir = Path(__file__).parent  # objects
            self.log_dir = current_dir.parent / "api_logs"
        else:
            self.log_dir = Path(log_dir)

        # Создаем директорию, если не существует
        self.log_dir.mkdir(exist_ok=True)

        # Создаем и настраиваем логер
        self.logger = self._create_logger()

    def _create_logger(self) -> logging.Logger:
        """Создает и настраивает логер"""
        # Создаем уникальное имя логера
        logger_name = f"api_tests.{self.api_name}"
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # Очищаем существующие обработчики
        logger.handlers.clear()

        # Создаем formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Создаем file handler
        log_file = self.log_dir / f"{self.api_name}.log"
        file_handler = logging.FileHandler(
            str(log_file),
            mode='a',
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        # Добавляем обработчик
        logger.addHandler(file_handler)
        logger.propagate = False

        return logger

    def info(self, message: str):
        """Логирование информационного сообщения"""
        self.logger.info(message)

    def debug(self, message: str):
        """Логирование отладочного сообщения"""
        self.logger.debug(message)

    def warning(self, message: str):
        """Логирование предупреждения"""
        self.logger.warning(message)

    def error(self, message: str, exc_info: bool = False):
        """Логирование ошибки"""
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message: str):
        """Логирование критической ошибки"""
        self.logger.critical(message)

    def get_log_file_path(self) -> Path:
        """Получить путь к файлу лога"""
        return self.log_dir / f"{self.api_name}.log"