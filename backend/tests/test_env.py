import os
from dotenv import load_dotenv

# Asegura que cargue las variables del .env
load_dotenv()

def test_env_vars_loaded():
    required = [
        "APP_NAME",
        "APP_ENV",
        "LOG_LEVEL",
        "SECRET_KEY",
        "JWT_SECRET",
        "JWT_ALG",
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "DATABASE_URL",
    ]
    for key in required:
        assert os.getenv(key), f"{key} is missing or empty"
