import os
import logging
from os import getenv, getcwd, environ
from functools import lru_cache
from pydantic import BaseSettings
from dash_bootstrap_components import icons
from pyapp.config import themes
from pydantic import BaseModel as PydanticBaseModel, BaseConfig

log = logging


class BaseModel(PydanticBaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True
        

class Settings(BaseSettings):
    
    environ['FLASK_APP'] = 'pyapp'
    
    project_name = 'pyapp'
    folder_pages = 'pages'
    folder_layouts = 'layouts'
    extensions = ['cache',  'session', 'auth', 'database',  'dash']

    environment: str = getenv("ENVIRONMENT", "development")
    folder_assets: str = f'{getcwd()}/assets'
    limit: int = int(getenv('LIMIT', 1500))
    base_url = os.getenv('BASE_URL', '/')
    redis_db = os.getenv('REDIS_HOST', 'redis://localhost:6379')
    
    sqlalchemy_database_uri = 'sqlite:///./data.db'
    
    nome_meses = ['JANEIRO','FEVEREIRO','MARÇO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']
    
    secret_session = '26595346-edd5-4637-b9a0-507727ad4d33'
    
    theme_default = 'BOOTSTRAP'
    
    theme_icon = icons.BOOTSTRAP
    
    themes= {
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
        env_nested_delimiter = '__'
        
    
@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()