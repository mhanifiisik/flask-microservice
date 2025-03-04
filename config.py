import os

class Config:
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 8080))
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

    # Simplified timeout settings (in seconds)
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
    KEEP_ALIVE_TIMEOUT = int(os.getenv('KEEP_ALIVE_TIMEOUT', 5))
    GRACEFUL_SHUTDOWN_TIMEOUT = int(os.getenv('GRACEFUL_SHUTDOWN_TIMEOUT', 5))

    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Security
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

    # Couchbase configuration
    COUCHBASE_HOST = os.getenv('COUCHBASE_HOST', 'couchbase://localhost')
    COUCHBASE_USER = os.getenv('COUCHBASE_USER', 'Administrator')
    COUCHBASE_PASSWORD = os.getenv('COUCHBASE_PASSWORD', 'password')
    COUCHBASE_BUCKET = os.getenv('COUCHBASE_BUCKET', 'travel-sample')
