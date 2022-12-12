from hashlib import md5
from dash import html, Input, Output, callback
from dash.exceptions import PreventUpdate
from pyapp.config import (
    BaseModel
)
import dash_bootstrap_components as dbc
from enum import Enum
from pyapp.utils.generic_util import StringUtil
from pyapp.core.pages.base import BaseIds

class MaskEnum(Enum):
    TELEFONE = '(__) _ ____-____'
    CEP = '_____-___'
    CNPJ = '__.___.___/____-__'

def transform_value_mask(value, mask:MaskEnum):

    return compile_mask(value, mask)

def compile_mask(value, mask:MaskEnum):
    text = str(mask.value)
    if not value:
        return text
    
    numero = StringUtil.to_number(value)
    
    if numero:
        data = [n for n in numero]

        text_resp = text.replace('_', '{}', len(data))

        return text_resp.format(*data)
    else:
        return text
    

class ComponentMaskProps(BaseModel):
    mask: MaskEnum
    aio_id: str

class ComponentMask:
    
    class Ids(BaseIds):
        component_mask: str
        
        def __init__(self, aio_id) -> None:
            super().__init__(aio_id, root='ComponentInputMaskAIO')
        
        
    ids : Ids

    def __init__(self, props: ComponentMaskProps, **kwargs) -> None:
        self.aio_id = md5(f'{__name__}-{props.aio_id}-{props.mask.value}'.encode()).hexdigest()
        
        self.ids = ComponentMask.Ids(self.aio_id)
        
        self.componet = props
        
        self.events()


    def layout(self, value=None):

        return html.Div([
            dbc.Input(
                id=self.ids.component_mask,
                value=transform_value_mask(value, self.componet.mask)
            )

        ])

    def events(self):
        
        @callback(
            Output(self.ids.component_mask, 'value'),
            Input(self.ids.component_mask, 'value')
        )
        def change(input):
            try:

                return transform_value_mask(input, self.componet.mask)
            except:
                raise PreventUpdate
            
            