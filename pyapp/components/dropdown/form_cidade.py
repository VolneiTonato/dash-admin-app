from typing import Optional, Any
from dash import html, dcc, Input, Output, callback
from pyapp.config import (
    BaseModel
)
from pyapp.core.pages.base import BaseIds
from pyapp.infra.entities.municipio import Municipio
from hashlib import md5

class ComponentDropdownCidadeProps(BaseModel):
    multi: Optional[bool] = True
    aio_id: str
    estado_id_component: str
    key_filter: Optional[int]
    fn: Optional[Any] = None


class ComponentDropdownCidade:
    
    class Ids(BaseIds):
        component_dropdown: str
        
        def __init__(self, aio_id) -> None:
            super().__init__(aio_id, root='ComponentDropdownCidadeAIO')
            
            
    ids: Ids = None
        

    def __init__(self, props: ComponentDropdownCidadeProps = None, **kwargs) -> None:
        
        self.aio_id = md5(f'{__name__}{props.aio_id}'.encode()).hexdigest()
        
        self.ids = ComponentDropdownCidade.Ids(self.aio_id)
        
        self.componente = props
        
        
        self.events()

    def load_municipios_by_id(self, estado_id):
        municipios = Municipio.find_by_estado(estado_id=estado_id)
        return [{'label': municipio.nome, 'value': municipio.id} for municipio in municipios]
        

    def layout(self, key_filter=None):
        self.componente.key_filter = key_filter
        return html.Div([
            dcc.Dropdown(
                id=self.ids.component_dropdown,
                multi=self.componente.multi,
                value=self.componente.key_filter or None
            ),

        ])

    def events(self):
        
        @callback(
            Output(self.ids.component_dropdown, 'options'),
            Output(self.ids.component_dropdown, 'value'),
            Input(self.componente.estado_id_component, 'value')
        )
        def change(codigo_uf):
            municipio_selected = self.componente.key_filter  if self.componente.key_filter else None
            if not codigo_uf:
                return [], municipio_selected
            
            return self.load_municipios_by_id(codigo_uf), municipio_selected
