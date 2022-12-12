from dash import html, dcc, Dash, Output, Input, no_update
from dash import strip_relative_path
from flask import Flask
from pyapp.config import get_settings
import pathlib
from importlib import import_module
from wheezy.routing.regex import RegexRoute
from wheezy.routing import curly
from pyapp.config import BaseModel
from urllib import parse
from typing import Optional, Any
from flask_login import logout_user, current_user
from typing import List, Tuple


_ID_CONTENT = "_custom_pages_content"
ID_LOCATION = "_custom_pages_location"
ID_LOCATION_REDIRECT = "_custom_pages_location_redirect"
_ID_STORE = "_custom_pages_store"
ID_DUMMY = "_custom_pages_dummy"


class NotPermitedException(Exception):
    pass

class NotFoundPageException(Exception):
    pass

class NotPagesLoadException(Exception):
    pass

class NotFoundLayoutException(Exception):
    pass

class PageData(BaseModel):
    urls_routes: list
    current_pathname : Optional[str]
    instance: Optional[Any]
    permission: Optional[str]
    param_layout = Optional[dict]
    query_layout = Optional[dict]


_LAYOUTS_REGISTRY: List[Tuple[str, object]] = []


page_container = html.Div(
    [
        dcc.Location(id=ID_LOCATION),
        dcc.Location(id=ID_LOCATION_REDIRECT),
        html.Div(id=_ID_CONTENT),
        dcc.Store(id=_ID_STORE, storage_type='session'),
        html.Div(id=ID_DUMMY),
    ])

    
def get_layout(key):
    for layouts in _LAYOUTS_REGISTRY:
        if layouts[0] == key:
            return layouts[1]
        
    raise NotFoundLayoutException

def init_app(app: Flask, dash_app: Dash):
    
    settings = get_settings()
    
    def url_query_string_to_dict(self, url):
            parse_data = parse.urlparse(url)
                    
            return dict(parse.parse_qsl(parse_data.query))
        
        
    def param_pathname_to_args(self, data):
        try:
            return data.values()
        except:
            return ()
        
    
    def component_not_pages():
        return html.Div([html.H1('Não foi possível importar as páginas!', style={'color': 'red'})])
    
    
    def component_not_found():
        return html.Div([html.H1('Não foi localizar a página desejada!', style={'color': 'red'})])
    
    def resolve_url(key, url):
    
        path = parse.urlparse(url).path

        r  = RegexRoute(curly.convert(key))

        hander, kwargs =  r.match_no_kwargs(path)
        
        # if len(kwargs):
            # return UrlTemplate.link(path), kwargs
        # return None
        
    def get_page(page_id:str):
        pass
    
    
    def import_layouts():
        folder_layouts = pathlib.Path(f'{settings.project_name}/{settings.folder_layouts}')
        for ext in folder_layouts.glob('**/layout.py'):
            module_name = str(ext).replace('/', '.').replace('.py', '')
            
            page_module = import_module(module_name)
            
            if 'LayoutPage' in dir(page_module):
                layout = page_module.LayoutPage()
                _LAYOUTS_REGISTRY.append((str(layout), layout))

    
    def get_import_pages():
        
    
        folder_pages = pathlib.Path(f'{settings.project_name}/{settings.folder_pages}')
        pages = []
        for ext in folder_pages.glob('**/*.py'):
        
            module_name = str(ext).replace('/', '.').replace('.py', '')
            
            page_module = import_module(module_name)
            
            if 'Page' in dir(page_module):
                page = page_module.Page()
                pages.append(page)
                
        return pages
    
    class Router():
        _is_running : bool = False
        _pages = []
        
        
        
        
        def __init__(self) -> None:
            self.router()
        
        
        def router(self):

            @app.before_first_request
            def first_run():
                import_layouts()
                self._pages = get_import_pages()
                
                
            
            @app.before_request
            def inner_router():
                if self._is_running:
                    return
                self._is_running = True
                
                self.events()
                
                
            
                
        def _is_auth(self):
            try:
                return current_user.is_authenticated
            except:
                return False
                
  
        def events(self):

            
            @dash_app.callback(
                [
                Output(_ID_CONTENT, "children"),
                Output(_ID_STORE, "data"),
                Output(ID_LOCATION_REDIRECT, 'pathname')
                ],
                Input(ID_LOCATION, "pathname"),
                Input(ID_LOCATION, "search"),

            )
            def update(pathname, search):

                layout = no_update
                data = no_update
                properties = {}
                
                
                try:
                    if not len(self._pages):
                        raise NotPagesLoadException()
                    
                    current_page = None
                    
                    relative = strip_relative_path(pathname)
                    
                    for page in self._pages:

                        path  = page.path
                         
                        if relative == path.strip('/'):
                            current_page = page
                            break
                    
                    if not current_page and relative != 'logout':
                        raise NotFoundPageException()

                    
                    is_auth = self._is_auth()
                    
                    if current_page:
                        properties  = dir(current_page)
                        
                    
                        layout = current_page.layout()
                        
                        if 'parent_layout' in properties:
                            layout = get_layout(current_page.parent_layout).layout(layout)
                        
                        data = {'title' : current_page.title}
                    

                    if relative in ['login'] and is_auth:
                        path = '/'
                        layout = no_update
                        data = no_update
                        
                    elif relative == 'logout':
                        if logout_user():
                            path = '/login'
                            layout = no_update
                            data = no_update
                
                    elif 'login_required' in properties and not relative in ['login', 'logout']:
                        if not current_user.is_authenticated:
                            path = '/login'
                            layout = no_update
                            data = no_update


                    return [layout, data, path]
                    
                except NotPagesLoadException as err:
                    return [component_not_pages(), no_update, no_update]
                except NotFoundPageException as err:
                    return [component_not_found(), no_update, no_update]
            

            dash_app.clientside_callback(
                '''
                function(data) {
                    document.title = data.title;
                    return '';
                }
                ''',
                Output(ID_DUMMY, "children"),
                Input(_ID_STORE, "data"),
            )
            
    Router()
            
  