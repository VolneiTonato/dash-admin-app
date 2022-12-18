from urllib import parse
from dash import get_relative_path
import dash_bootstrap_components as dbc

   
def _generate_bread_crumbs(url:str):
    
    if not '/' in url:
        return []
    
    urls = parse.urlparse(url).path.split('/')
    breads = []
    
    urls_filters = list(filter(lambda u : u != '', urls))

    if len(urls_filters):
        
        size = len(urls_filters) - 1

        breads.append({'label': 'home', 'href': get_relative_path(f'/')})
    
        for idx, link in enumerate(urls_filters):
            label = link
            
            link_alternative = link

            obj = {'label': label, 'href': get_relative_path(f'/{link_alternative}')}

            if size == idx:
                obj.update({'active': True})
            
            breads.append(obj)
        

    return breads


class ComponentBreadCrumbs:


    def __init__(self, **kwargs) -> None:
        pass


    def layout(self, current_pathname=None):
        try:
            items = _generate_bread_crumbs(current_pathname)
            if len(items):
                return dbc.Breadcrumb(
                    items=items
                )
            return None
        except:
            return None    