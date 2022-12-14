
import os
import logging
from os import  getcwd, environ
from functools import lru_cache
from typing import Optional
from dash_bootstrap_components import icons
from pyapp.config import themes
from pydantic import BaseModel as PydanticBaseModel, BaseConfig, BaseSettings, Field

log = logging


class BaseModel(PydanticBaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True
        
class GlobalConfig(BaseSettings):
    """Global configurations."""

    # define global variables with the Field class
    ENV_STATE: Optional[str] = Field(None, env="ENV_STATE")

    REDIS_HOST: Optional[str] = None
    
    PROJECT_NAME:str  = 'pyapp'
    FOLDER_PAGES = 'pages'
    FOLDER_LAYOUTS = 'layouts'
    EXTENSIONS = ['cache',  'session', 'auth', 'database',  'dash']
    FOLDER_ASSETS: str = f'{getcwd()}/assets'
    LIMIT_QUERY: int = 1500
    BASE_URL: str = '/'
        
    SQLALCHEMY_DATABASE_URI: str = None

    NOME_MESES = ['JANEIRO','FEVEREIRO','MARÇO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']
    
    SECRET_SESSION = '26595346-edd5-4637-b9a0-507727ad4d33'
    
    THEME_DEFAULT = 'BOOTSTRAP'
    
    THEME_ICON = icons.BOOTSTRAP
    
    THEMES = {
        'BOOTSTRAP': themes.BOOTSTRAP,
        'CERULEAN': themes.CERULEAN,
        'COSMO' : themes.COSMO,
        'CYBORG': themes.CYBORG,
        'DARKLY' :  themes.DARKLY,
        'FLATLY': themes.FLATLY,
        'JOURNAL': themes.JOURNAL,
        'LITERA': themes.LITERA,
        'LUMEN': themes.LUMEN,
        'LUX': themes.LUX,
        'MATERIA': themes.MATERIA,
        'MINTY': themes.MINTY,
        'MORPH': themes.MORPH,
        'PULSE': themes.PULSE,
        'QUARTZ': themes.QUARTZ,
        'SANDSTONE': themes.SANDSTONE,
        'SIMPLEX': themes.SIMPLEX,
        'SKETCHY':themes.SKETCHY,
        'SLATE': themes.SLATE,
        'SOLAR': themes.SOLAR,
        'SPACELAB': themes.SPACELAB,
        'SUPERHERO': themes.SUPERHERO,
        'UNITED': themes.UNITED,
        'VAPOR': themes.VAPOR,
        'YETI': themes.YETI,
        'ZEPHYR': themes.ZEPHYR,
        'FONTAWESOME_5': themes.FONTAWESOME_5
    }

    class Config:
        """Loads the dotenv file."""
        env_nested_delimiter = '__'
        env_file: str = ".env"


class DevConfig(GlobalConfig):
    """Development configurations."""

    class Config:
        env_prefix: str = "DEV_"
        env_file: str = ".dev"


class ProdConfig(GlobalConfig):
    """Production configurations."""

    class Config:
        env_prefix: str = "PROD_"
        env_file: str = ".prod"
        
class DockerConfig(GlobalConfig):
    """Production configurations."""

    class Config:
        env_prefix: str = "DOCKER_"
        env_file: str = ".env_docker"



class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig()

        elif self.env_state == "prod":
            return ProdConfig()
        
        elif self.env_state == "docker":
            return DockerConfig()


@lru_cache()
def get_settings() -> GlobalConfig:
    log.info("Loading config settings from the environment...")
    return FactoryConfig(GlobalConfig().ENV_STATE)()