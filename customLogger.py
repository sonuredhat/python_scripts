import logging
from datetime import datetime
import uuid

class CustomLogger:
    class LogUUIDFilter(logging.Filter):
        def __init__(self, uuid_value):
            super().__init__()
            self.uuid = uuid_value

        def filter(self, record):
            record.logUUID = self.uuid
            return True

    def __init__(self, name, enabled_levels="INFO"):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False  # 👈 Important: prevent double logging

        # Generate unique UUID
        self.logUUID = str(uuid.uuid4())
        self.uuid_filter = self.LogUUIDFilter(self.logUUID)

        # --- Console Handler ---
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s_%(logUUID)s - %(message)s - [%(funcName)s:%(filename)s:%(lineno)d]"
        )
        ch.setFormatter(console_formatter)
        ch.addFilter(self.uuid_filter)
        self.logger.addHandler(ch)

        # --- File Handler ---
        timeStamp = datetime.now().strftime("%Y-%m-%d")
        file_path = f'/var/log/{self.name}_{timeStamp}.log'
        fh = logging.FileHandler(file_path)
        fh.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s_%(logUUID)s - %(message)s - [%(funcName)s:%(filename)s:%(lineno)d]"
        )
        fh.setFormatter(file_formatter)
        fh.addFilter(self.uuid_filter)
        self.logger.addHandler(fh)

        self.enabled_levels = enabled_levels or {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

    def _is_enabled(self, level_name):
        return level_name in self.enabled_levels

    def log_debug(self, message):
        if self._is_enabled("DEBUG"):
            self.logger.debug(message, stacklevel=2)

    def log_info(self, message):
        if self._is_enabled("INFO"):
            self.logger.info(message, stacklevel=2)

    def log_warning(self, message):
        if self._is_enabled("WARNING"):
            self.logger.warning(message, stacklevel=2)

    def log_error(self, message):
        if self._is_enabled("ERROR"):
            self.logger.error(message, stacklevel=2)

    def log_critical(self, message):
        if self._is_enabled("CRITICAL"):
            self.logger.critical(message, stacklevel=2)


# Initialize the logger
logger = CustomLogger("correctCallRecording", enabled_levels={"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})
# Set the logger to use the custom logger
logging.basicConfig(level=logging.DEBUG, handlers=[logger.logger.handlers[0]], format="%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(funcName)s:%(lineno)d]")

def raiseLog():
    logger.log_info("this is info Log")
    logger.log_warning("this is warning Log")

if __name__ == "__main__":
    raiseLog()


