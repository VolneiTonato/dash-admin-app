from typing import Optional
from dash import html, dcc
from pyapp.config import (
    BaseModel
)
from pyapp.core.pages.base import BaseIds
from pyapp.ext.cache import cache
from pyapp.infra.entities.estado import Estado
from hashlib import md5


class ComponentDropdownEstadoProps(BaseModel):
    key_filter: Optional[str] = None
    aio_id: str

class ComponentDropdownEstado:
    
    class Ids(BaseIds):
        component_dropdown: str
        
        def __init__(self, aio_id) -> None:
            super().__init__(aio_id, root='ComponentDropdownEstadoAIO')
            
    ids: Ids
    
    def __init__(self, props: ComponentDropdownEstadoProps = None, **kwargs) -> None:
        
        self.aio_id = md5(f'{__name__}{props.aio_id}'.encode()).hexdigest()
        
        self.ids = ComponentDropdownEstado.Ids(self.aio_id)

        
        self.component = props
        
    
    @cache.memoize(60*2)
    def load_data(self):
        self._estados = [{'label': estado.nome, 'value': estado.id} for estado in Estado.query.all()]

    
    def layout(self, key_filter=None):
        self.load_data()
        
        self.component.key_filter = key_filter
        
        return html.Div([
            dcc.Dropdown(
                options=self._estados,
                id=self.ids.component_dropdown,
                value=self.component.key_filter or None
            )
        ])
