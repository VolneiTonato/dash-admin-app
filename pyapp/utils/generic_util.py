import re
from typing import Union
from pyapp.core.decorator import type_check
from pydantic import ValidationError
from dash.html import Div

class ErrorValidationModel:
    
    def message(error: ValidationError, Component=Div):
        if isinstance(error, ValidationError):
            message = []
            err = {}
            for err in error.errors():
                m = ''
                if err.get('type') in ['type_error.none.not_allowed', 'value_error.missing']:
                    m = f'{err.get("loc")[0]} é obrigatório'
                else:
                    m = str(err.get('msg'))
                message.append(Component(f"* {m}"))
                
            return message
        return Component(str(error))
    

class StringUtil:

    @type_check
    def to_number(value: Union[str, int]):
        r = re.compile('\D')
        return r.sub('', value)
    
    


class ObjectUtil:
    
    def get_selected_option_dropdown(value, options):
        """
        Current value dropdown
        State options dropdown
        
        
        Example:
        
        value = 43
        
        options = [
            {'label': 'RIO GRANDE DO SUL', 'value': 43}, 
            {'label': 'MATO GROSSO DO SUL', 'value': 50}, 
            {'label': 'MATO GROSSO', 'value': 51}
        ]
        
        ObjectUtil.get_value_options_dropdown(value, options)
        
        [{'label': 'RIO GRANDE DO SUL', 'value': 43}]
        
        """
        try:
            return list(filter(lambda option: str(option['value']) == str(value), options))
        except:
            return []
    
    def is_index(data, idx):
        try:
            data[idx]
            return True
        except:
            return False
    

    def getattr_model(obj, paths:str, default = None):
        try:
                        
            def get_getmodel(model, property):
                return model.__getattribute__(property)
            
            if '.' in paths:
                columns = paths.split('.')
            elif isinstance(paths, str):
                columns = [paths]
            
            current = obj

            for column in columns:
                current = get_getmodel(current, column)

                
            return current
        except:
            return default