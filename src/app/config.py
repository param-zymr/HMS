"""Genaral Configuration"""
import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    DB_NAME = str(os.getenv("DB_NAME", "dev_db"))
    DB_USER = str(os.getenv("DB_USER", "dev_user"))
    DB_PASSWORD = str(os.getenv("DB_PASSWORD", "devuser123"))
    DB_URL = str(os.getenv("DB_URL", "localhost"))
    DB_PORT = str(os.getenv("DB_PORT", "5432"))
    SQLALCHEMY_DATABASE_URI = str(os.getenv("DATABASE_CONN_URL", \
        "postgresql+psycopg2://dev_user:devuser123@localhost:5432/dev_db"))
    APP_HOST = str(os.getenv("APP_HOST", "localhost"))
    APP_PORT = str(os.getenv("APP_PORT", "5000"))
    PASSWORD_PEPPER = str(os.getenv("PASSWORD_PEPPER", "$2b$12$sdBcmAcmqs7tSv.GIapVye"))
    JSON_SORT_KEYS = False
    APPOINTMENT_OFFSET = int(os.getenv("APPOINTMENT_OFFSET", "10")) #appointment offset (mins)
    APPOINTMENT_MIN_TIME = int(os.getenv("APPOINTMENT_MIN_TIME", "15")) #minimun appointment duration (mins)
    JWT_ACCESS_TOKEN_SECRET_KEY = str(os.getenv("JWT_ACCESS_TOKEN_SECRET_KEY", \
        "$2b$12$u7C3BgG7GorzkO0tSMJdUO"))
    JWT_REFRESH_TOKEN_SECRET_KEY = str(os.getenv("JWT_REFRESH_TOKEN_SECRET_KEY", \
        "$2b$12$IENesCTc6eFpINkjqckrHO"))
    JWT_ACCESS_TOKEN_EXPIRE_TIME = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_TIME", "30")) #duration in mins
    JWT_REFRESH_TOKEN_EXPIRE_TIME = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_TIME", "30")) #duration in days
    JWT_REFRESH_TOKEN_TIMEOUT = int(os.getenv("JWT_REFRESH_TOKEN_TIMEOUT", "90")) #duration in days
    JWT_ALGORITHM = str(os.getenv("JWT_ALGORITHM", "HS256"))
    SMTP_SERVER = str(os.getenv("SMTP_SERVER", "smtp.gmail.com"))
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = str(os.getenv("SMTP_USERNAME", "dev@gmail.com"))
    SMTP_PASSWORD = str(os.getenv("SMTP_PASSWORD", "dev123"))
    SMTP_DEFAULT_SENDER = str(os.getenv("SMTP_DEFAULT_SENDER", "Developer<dev@gmail.com>"))
    TEMPLATE_DIR = "./src/app/templates"
    USER_CATAGORY_PREFIX = {"manager":"MNGR","doctor":"DOC","patient":"PAT",\
        "receptionist":"REC"}
    #CELERY Settings
    CELERY_BROKER_URL = "redis://localhost:6379"
    CELERY_RESULT_BACKEND = "redis://localhost:6379"
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_SERIALIZER = 'json'
    # CELERY_TASK_IGNORE_RESULT = True
    
    LOG_FILE_PATH = "./src/app/logs/app_logs.log"
    LOG_LEVEL = str(os.getenv("LOG_LEVEL", "DEBUG"))
    LOG_FORMAT = "[%(asctime)s] [%(threadName)s:%(thread)d] \
[%(filename)s.%(funcName)s:%(lineno)d] %(levelname)s - %(message)s"
    LOG_DATE_FMT = "%d/%m/%Y %I:%M:%S %p"
    LOG_DICT_CONFIG = {
        'version': 1,
        'formatters': {
            'default': {'format': LOG_FORMAT, 'datefmt': LOG_DATE_FMT}
        },
        'handlers': {
            'console': {
                'level': LOG_LEVEL,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': LOG_LEVEL,
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': LOG_FILE_PATH,
                'maxBytes': 2097152, #2 MB(2 * 1024 * 1024)
                'backupCount': 0
            }
        },
        'loggers': {
            'default': {
                'level': LOG_LEVEL,
                'handlers': ['console', 'file']
            }
        },
        'disable_existing_loggers': True
    }
app_settings = Settings()
