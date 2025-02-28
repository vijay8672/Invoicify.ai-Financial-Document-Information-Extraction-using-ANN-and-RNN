import logging  # Standard Python logging module
import os  # OS module to handle file paths
import glob  # For pattern-based file searching
from datetime import datetime  # To generate unique timestamp-based log files
from logging.handlers import RotatingFileHandler  # Handles rotating log files
from pythonjsonlogger import jsonlogger  # Formats logs in JSON format

# Optional: Google Cloud Logging (only if available)
try:
    from google.cloud import logging as cloud_logging  # Google Cloud Logging client
    GCP_LOGGING_AVAILABLE = True  # Flag to check if GCP logging is available
except ImportError:
    GCP_LOGGING_AVAILABLE = False  # If Google Cloud SDK is not installed, disable GCP logging

# 1️⃣ Get Environment (Defaults to 'development' if not set)
APP_ENV = os.getenv("APP_ENV", "development")

# 2️⃣ Create Logger with the name "Invoicify.ai"
logger = logging.getLogger("Invoicify.ai")
# Set log level based on environment (DEBUG for production, INFO for development)
logger.setLevel(logging.DEBUG if APP_ENV == "production" else logging.INFO)

# 3️⃣ Define Log Format (JSON format for better readability)
formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s %(lineno)d"
)

# 4️⃣ Setup Log Directory
log_dir = os.path.join(os.getcwd(), "logs")  # Create a "logs" directory in the current working directory
os.makedirs(log_dir, exist_ok=True)  # Ensure the logs directory exists (create if it doesn’t)

# 5️⃣ Generate a New Log File for Each Run
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Example format: 2024-02-28_15-30-00
log_file = os.path.join(log_dir, f"log_{timestamp}.log")  # Log file path with timestamp

# Configure Rotating File Handler
file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=5, mode="w")
file_handler.setFormatter(formatter)  # Apply JSON formatting to log entries
logger.addHandler(file_handler)  # Attach file handler to logger

# 6️⃣ Console Logging for Development (Displays logs in the terminal)
console_handler = logging.StreamHandler()  # Create a handler that writes log messages to sys.stderr
console_handler.setFormatter(formatter)  # Apply JSON formatting
logger.addHandler(console_handler)  # Attach console handler to logger

# 7️⃣ Google Cloud Logging (Only if credentials exist)
if GCP_LOGGING_AVAILABLE and os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    client = cloud_logging.Client()  # Create a Google Cloud Logging client
    cloud_handler = cloud_logging.handlers.CloudLoggingHandler(client)  # Create a handler for GCP logging
    cloud_handler.setFormatter(formatter)  # Apply JSON formatting
    logger.addHandler(cloud_handler)  # Attach GCP log handler to logger

# 8️⃣ Cleanup Old Log Files (Keep Only Last 5)
log_files = sorted(glob.glob(os.path.join(log_dir, "log_*.log")), reverse=True)  # Get list of all log files

# If there are more than 5 logs, delete the oldest ones
if len(log_files) > 5:
    for old_log in log_files[5:]:  # Select logs beyond the last 5
        try:
            if old_log in [handler.baseFilename for handler in logger.handlers if isinstance(handler, RotatingFileHandler)]:
                continue  # Skip deleting the currently active log file
            
            os.remove(old_log)  # Delete old log file
        except PermissionError:
            print(f"Skipping deletion of {old_log} (file is in use)")
            
if __name__=="__main__":
    # 9️⃣ Example Logs (These logs will appear in both console and log files)
    logger.info("User logged in", extra={"user": "JohnDoe", "action": "login"})
    logger.error("Database connection failed", extra={"db": "Postgres", "status": "down"})