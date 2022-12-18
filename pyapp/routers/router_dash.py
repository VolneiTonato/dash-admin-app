from dash import html, dcc, Dash, Output, Input, no_update
from dash import strip_relative_path, get_relative_path
from flask import Flask
from pyapp.config import get_settings, BaseModel
import pathlib
import flask
from importlib import import_module
from wheezy.routing.regex import RegexRoute
from wheezy.routing import curly
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

    def url_query_string_to_dict(url):
            parse_data = parse.urlparse(url)
                    
            return dict(parse.parse_qsl(parse_data.query)) or {}
        
    
    def component_not_pages():
        return html.Div([html.H1('Não foi possível importar as páginas!', style={'color': 'red'})])
    
    
    def component_not_found():
        return html.Div([html.H1('Não foi localizar a página desejada!', style={'color': 'red'})])
    
    
    def import_layouts():
        folder_layouts = pathlib.Path(f'{settings.PROJECT_NAME}/{settings.FOLDER_LAYOUTS}')
        for ext in folder_layouts.glob('**/layout.py'):
            module_name = str(ext).replace('/', '.').replace('.py', '')
            
            page_module = import_module(module_name)
            
            if 'LayoutPage' in dir(page_module):
                layout = page_module.LayoutPage()
                _LAYOUTS_REGISTRY.append((str(layout), layout))

    
    def get_import_pages():

        folder_pages = pathlib.Path(f'{settings.PROJECT_NAME}/{settings.FOLDER_PAGES}')
        pages = []
        for ext in folder_pages.glob('**/*.py'):
        
            module_name = str(ext).replace('/', '.').replace('.py', '')
            
            page_module = import_module(module_name)
            
            if 'Page' in dir(page_module):
                page = page_module.Page()
                pages.append(page)
                
        return pages
    
    class Router():
                
        def __init__(self) -> None:
            self._pages = []
            self._is_running = False
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
            
        def get_page_and_kwargs(self, pathname):
            relative = strip_relative_path(get_relative_path(pathname))
            current_page = None
            kwargs_page = {}
            for page in self._pages:
                try:
                    current_page = next(filter(lambda p : relative == p.path.strip('/') if p.path else None, self._pages))
                except:
                    pass
                if not current_page:
                    for _path in page.template_path:
                        if relative == _path.strip('/'):
                            page.path = _path
                            current_page  = page
                            
                            break
                        
                    if not current_page:
                        for _path in page.template_path:
                            r = RegexRoute(curly.convert(_path))
                        
                            if r:
                                hander, kwargs_page = r.match_no_kwargs(pathname)
                                if kwargs_page:
                                    page.path = pathname
                                    current_page = page
                                    break
                            
            return (current_page, kwargs_page or {})
  
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
                    
                    kwargs_query_page = {}
                    
                    args_page = {}
                    
                    if pathname != '' and search != '':
                        full_url = f'{pathname}{search}'

                        kwargs_query_page = url_query_string_to_dict(full_url)
                    
                    current_page = None
                   
                    relative = strip_relative_path(pathname)

                    current_page, args_page = self.get_page_and_kwargs(pathname)
                    
                    
                    if not current_page and relative != 'logout':
                        raise NotFoundPageException()

                    
     
                    is_auth = self._is_auth()
                    
                    if current_page:
                        path = current_page.path
                        
                        properties  = dir(current_page)
                        
                    
                        layout = current_page.layout(*args_page.values(), **kwargs_query_page)
                        
                        if 'parent_layout' in properties:
                            layout = get_layout(current_page.parent_layout).layout(layout)
                        
                        data = {'title' : current_page.title}
                    

                    if relative in ['login'] and is_auth:
                        path = get_relative_path('/')
                        layout = no_update
                        data = no_update
                        
                    elif relative == 'logout':
                        if logout_user():
                            path = get_relative_path('/login')
                            layout = no_update
                            data = no_update
                
                    elif 'login_required' in properties and not relative in ['login', 'logout']:
                        if not is_auth:
                            path = get_relative_path('/login')
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
            
  