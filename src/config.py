import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
SOURCE_DB_PATH = os.path.join(DATA_DIR, 'source.db')
TARGET_DB_PATH = os.path.join(DATA_DIR, 'target.db')

# Database configurations
SOURCE_DB_CONNECTION = f'sqlite:///{SOURCE_DB_PATH}'
TARGET_DB_CONNECTION = f'sqlite:///{TARGET_DB_PATH}'

# Spark configurations
SPARK_CONFIG = {
    'spark.app.name': 'HealthcareLogProcessor',
    'spark.executor.memory': '2g',
    'spark.executor.cores': '2',
    'spark.driver.memory': '2g'
}

# Log processing configurations
BATCH_SIZE = 1000
LOG_COLUMN_NAME = 'log_text'  # Source database log text column name
SOURCE_TABLE_NAME = 'etl_logs'  # Source database table name
