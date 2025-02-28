import logging
import traceback
from logging_setup.logger import logger

# Configure logger
logger = logging.getLogger("Invoicify.ai")

class CustomException(Exception):
    """Custom exception class that handles all types of application errors with logging."""

    def __init__(self, message, category="General", log_level=logging.ERROR, log_exception=True):
        """
        Initialize the exception with a message, category (e.g., "Database", "File", "API"), and log level.
        
        :param message: Error message
        :param category: Type of error (e.g., "Database", "File", "API")
        :param log_level: Logging level (default: ERROR)
        :param log_exception: Whether to log the exception automatically (default: True)
        """
        super().__init__(message)
        self.category = category
        self.log_level = log_level

        # Log only if explicitly allowed
        if log_exception:
            self.log_exception()

    def log_exception(self):
        """Logs the exception with category and traceback details (if applicable)."""
        log_message = f"[{self.category}] {self.args[0]}"
        
        # Get traceback only if inside an `except` block
        trace = traceback.format_exc()
        if trace == "NoneType: None\n":  # Means it wasn't raised inside an `except` block
            trace = None

        logger.log(self.log_level, log_message, extra={"category": self.category, "traceback": trace})


# **Example Usage**
if __name__ == "__main__":
    try:
        raise CustomException("Unable to connect to PostgreSQL server.", category="Database", log_level=logging.CRITICAL)
    except CustomException as e:
        print(f"Handled Exception: {e}")

    try:
        raise CustomException("API request timed out.", category="API", log_level=logging.WARNING)
    except CustomException as e:
        print(f"Handled Exception: {e}")

    # Example without logging
    try:
        raise CustomException("Validation failed: Missing email.", category="Validation", log_exception=False)
    except CustomException as e:
        print(f"Handled Exception (without logging): {e}")
