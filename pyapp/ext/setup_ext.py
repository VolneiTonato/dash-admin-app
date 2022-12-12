
from importlib import import_module
import pathlib
from flask import Flask
from pyapp.config import get_settings
from pyapp.utils.generic_util import ObjectUtil


def load_extensions(app: Flask):
    settings = get_settings()
    
    folder = f'{settings.project_name}/ext'
    
    for ext in settings.extensions:
        file = pathlib.Path(f'{folder}/{ext}.py')

        data = str(file)
        
        module_name = data.replace('/', '.').replace('.py', '')         

    
        ext = import_module(module_name)
        
        if 'init_app' in dir(ext):
            ext.init_app(app)
            
            
def load_entities(app:Flask, args_command=None):
    settings = get_settings()
    
    
    with app.app_context() as ctx:
        from .database import db
        
        
        folder = f'{settings.project_name}/infra/entities'
        
        for entity in pathlib.Path(folder).glob('*.py'):
            
            data = str(entity)
            
            module_name = data.replace('/', '.').replace('.py', '') 

            import_module(module_name)
        

        if ObjectUtil.getattr_model(args_command, 'command'):
            from pyapp.infra.config import commands
            if ObjectUtil.getattr_model(args_command, 'command') == 'populate-db':
                commands.populate_estados_database()
                commands.populate_municipios_database()
                commands.populate_clientes_database()
                
            elif ObjectUtil.getattr_model(args_command, 'command') == 'create-db':
                db.create_all()
            
            elif ObjectUtil.getattr_model(args_command, 'command') == 'drop-db':
                db.drop_all()
                
            print('*** commando OK')
            exit()