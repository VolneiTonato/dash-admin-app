from scss import Compiler
import base64
from dash.html import Link, Div, Script
import pathlib
import re
from csscompressor import compress



class StyleComponentUtil:
    components = []
    
    def __init__(self) -> None:
        self.components = []
    
    def _current_folder(self, file):
        return pathlib.Path(file).parent
    
    def __add_component_dash(self, data, is_base64:bool=False):
        
        href = None
        if is_base64:
            href = f"data:text/css;base64,{data}"
        else:
            href = data
            
        self.components.append(Link(rel='stylesheet',
                          href=href))
        
        
    
    def __replace_rule_css(self, replace_value, tamanho):
        def inner(va:re.Match):
            data = va.group()
            if data:
                content = data[0:tamanho]
                separator = data[tamanho:tamanho + 1]
                rest = data[tamanho:]
                compile = re.compile(r'[0-9A-Za-z-]')
                if not re.match(compile, separator):
                    return replace_value + rest
                return data
        return inner
        
        
        
    @property
    def link_css(self):
        return Div(self.components)
    
    
    def add_js_external(self, url):
        self.components.append(Script(src=url, type='text/javascript'))
        return self
    
    def add_file_external(self, url):
        self.__add_component_dash(url)
        return self
    
    def add_file_scss(self, name, folder_file, is_base64 = False, **kwargs):
        folder = f"{self._current_folder(folder_file)}/{name}"

        
        with open(folder, 'rb') as file:
            
            text = file.read().decode()

            if kwargs:
                for key, value  in kwargs.items():
                    pattern = re.compile(key + '?.+{')

                    text = re.sub(pattern, self.__replace_rule_css(replace_value=value, tamanho=len(key)), text)

            text = Compiler().compile_string(text)

            if is_base64:
                style = base64.encodestring(text.encode()).decode()
            else:
                style = text
                
        
                
        self.__add_component_dash(data=compress(style), is_base64=is_base64)
        
        return self
        