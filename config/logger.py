import logging
from pathlib import Path


class APILogger:
    """Логер для записи результатов выполнения API тестов."""

    def __init__(self, api_name: str, log_dir: str = None):
        """
        Инициализирует логер для указанного API.

        Args:
            api_name: Имя API для логирования
            log_dir: Директория для сохранения логов
        """
        self.api_name = api_name

        # Определяем путь к директории логов
        if log_dir is None:
            current_dir = Path(__file__).parent
            self.log_dir = current_dir.parent / "api_logs"
        else:
            self.log_dir = Path(log_dir)

        # Создаем директорию, если не существует
        self.log_dir.mkdir(exist_ok=True)

        # Создаем и настраиваем логер
        self.logger = self._create_logger()

    def _create_logger(self) -> logging.Logger:
        """Создает и настраивает объект логера."""
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

        # Создаем file handler с режимом перезаписи
        log_file = self.log_dir / f"{self.api_name}.log"
        file_handler = logging.FileHandler(
            str(log_file),
            mode='w',
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        # Добавляем обработчик
        logger.addHandler(file_handler)
        logger.propagate = False

        return logger

    def info(self, message: str):
        """Записывает информационное сообщение в лог."""
        self.logger.info(message)

    def debug(self, message: str):
        """Записывает отладочное сообщение в лог."""
        self.logger.debug(message)

    def warning(self, message: str):
        """Записывает предупреждение в лог."""
        self.logger.warning(message)

    def error(self, message: str, exc_info: bool = False):
        """
        Записывает сообщение об ошибке в лог.

        Args:
            message: Текст сообщения об ошибке
            exc_info: Флаг для включения информации об исключении
        """
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message: str):
        """Записывает сообщение о критической ошибке в лог."""
        self.logger.critical(message)

    def get_log_file_path(self) -> Path:
        """Возвращает путь к файлу лога."""
        return self.log_dir / f"{self.api_name}.log"