from pathlib import Path
from typing import Union

from pydantic import AnyHttpUrl, DirectoryPath, PostgresDsn
from pydantic_settings import BaseSettings

from app.utils.type_extra import SQLiteDsn
from app.core.utils import return_private_key

class Settings(BaseSettings):
    # service_name: "Authentication_service"
    # database_url: Union[PostgresDsn, SQLiteDsn]
    # postgres_url:PostgresDsn
    # port: int = 8001
    debug: bool = True
    # secret_key: str
    # secret_key:"jajaja"
    # base_dir: DirectoryPath = Path(__file__).resolve().parent.parent.parent
    # reload: bool = True
    # factory: bool = True
    db_echo: bool = False
    # host: str = "localhost"
    # workers_count: int = 4
    # social_base_url: AnyHttpUrl
    allowed_origins: list = ["*"]
    # auth_private_key: str
    # sentry_logger_url: AnyHttpUrl
    auth_private_key: str = return_private_key()
    # class Config:
    #     env_prefix = "ktutors_env_"
    class Config:
        env_prefix = "ktutors_env_"


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
