from hashlib import md5
from typing import Optional, Tuple
from dash import html, Input, Output, callback, State
from dash.exceptions import PreventUpdate
from pyapp.config import (
    BaseModel
)
import dash_bootstrap_components as dbc
from pyapp.core.pages.base import BaseIds
import re


class DecimalProps(BaseModel):
    format_number: Optional[Tuple[int, int]] = (10, 4)
    sep: Optional[str] = '.'

class ComponentCurrencyProps(DecimalProps):
    aio_id: str
    
    
def transform_value_mask(value, props:DecimalProps):
    
    try:
        if not value:
            raise Exception
        
        value = str(value)


        format_number = props.format_number
        
        sep = props.sep

        value = re.sub(r'[^\d.,]', '', value)

        total_dot = re.findall(r'\.', value)

        total_virgula  = re.findall(r',', value)

        if len(total_virgula) > 0:
            if len(total_dot) > 0:
                value = re.sub(r',', '', str(value))
            else:
                value = re.sub(r',', '.', str(value))
                
        total_dot = re.findall(r'\.', value)

        if len(total_dot) > 1:
            value = value.replace('.', '', len(total_dot) - 1)
            
        total_dot = re.findall(r'\.', value)
            
        if len(total_dot):
            part = value.split('.')
            
            value = f'{part[0][0:format_number[0]]}{sep}{part[1][0:format_number[1]]}'
        else:
            value = f'{value[0:format_number[0]]}'

        return str(value)
        
    except:
        return ''



class ComponentCurrency:
    
    class Ids(BaseIds):
        component_currency: str
        
        def __init__(self, aio_id) -> None:
            super().__init__(aio_id, root='ComponentInputCurrencyAIO')
        
        
    ids : Ids

    def __init__(self, props: ComponentCurrencyProps, **kwargs) -> None:
        self.aio_id = md5(f'{__name__}-{props.aio_id}'.encode()).hexdigest()
        
        self.ids = ComponentCurrency.Ids(self.aio_id)
        
        self.on_load = False
        
        self.componet = props
        
        self.events()


    def layout(self, value=None):
        
        self.on_load = True

        return html.Div([
            dbc.Input(
                id=self.ids.component_currency,
                value=transform_value_mask(value, self.componet),
                type='text'
            )

        ])

    def events(self):
        
        @callback(
            Output(self.ids.component_currency, 'value'),
            Input(self.ids.component_currency, 'value')
        )
        def change(input):
            try:
                if self.on_load:
                    self.on_load = False
                    raise PreventUpdate
                return transform_value_mask(input, self.componet)
            except:
                raise PreventUpdate
            
            