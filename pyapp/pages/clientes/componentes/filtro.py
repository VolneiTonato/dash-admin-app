import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import html, Input, Output, State, callback, no_update, dcc, ctx
from pyapp.infra.entities.cliente import Cliente
from pyapp.pages.clientes.schema.ids import FitroComponentClienteIds
from pyapp.components.dropdown.form_estado import ComponentDropdownEstado, ComponentDropdownEstadoProps
from pyapp.components.dropdown.form_cidade import ComponentDropdownCidade, ComponentDropdownCidadeProps
from pyapp.config import BaseModel
from pyapp.utils.generic_util import ObjectUtil
from typing import Optional, Union


class SessionForm(BaseModel):
    text: Optional[Union[str, None]]
    estado_id: Optional[Union[str, None]]
    municipio_id: Optional[Union[str, None]]
    text_label: Optional[Union[list, None]]
    municipio_label: Optional[Union[list, None]]
    estado_label: Optional[Union[list, None]]
    
    def do_validator(self):
        values = []
        for property in self.__annotations__:
            values.append(getattr(self, property))
            
        if len(list(filter(lambda row : row, values))) > 0:
            return True
        raise Exception('informe algum valor')

class Filtro:
    
    
    
    ids: FitroComponentClienteIds

    def __init__(self) -> None:
        
        self.ids = FitroComponentClienteIds()
        
        self.current_form: SessionForm = None

        self.componentEstado = ComponentDropdownEstado(
            ComponentDropdownEstadoProps(
                aio_id=self.ids.aio_id
            )
        )
        
        self.componentCidade = ComponentDropdownCidade(
            ComponentDropdownCidadeProps(
                estado_id_component=self.componentEstado.ids.component_dropdown,
                multi=False,
                aio_id=self.ids.aio_id
            )
        )

        self.events()
        
        

    def layout(self, current_form_state=None):
        
        if current_form_state:
            self.current_form = SessionForm(**current_form_state)

        return dbc.Form([
            dbc.Card(
                [
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Digite aqui o que você deseja filtrar"),
                            dcc.Dropdown(
                                id=self.ids.input_search, 
                                options=ObjectUtil.getattr_model(self.current_form, 'text_label', default=[]), 
                                value=ObjectUtil.getattr_model(self.current_form, 'text'), 
                                searchable=True)
                        ], width=12, class_name='mb-3'),
                        
                        dbc.Col([
                            dbc.Label("Estado"),
                            self.componentEstado.layout(ObjectUtil.getattr_model(self.current_form, 'estado_id'))
                        ], width=6, class_name='mb-3'),
                        
                        dbc.Col([
                            dbc.Label("Cidade"),
                            self.componentCidade.layout(ObjectUtil.getattr_model(self.current_form, 'municipio_id'))
                        ], width=6, class_name='mb-3'),

                    ]),
                ], body=True),
            dbc.Card(
                [
                    dbc.Row(
                        dbc.Col([
                            dbc.Button('Buscar', class_name='me-2', size="lg", color='info', id=self.ids.btn_search, n_clicks=0),
                            dbc.Button('Limpar', class_name='me-2', size="lg", color='danger', id=self.ids.btn_clear, n_clicks=0),

                        ], width=12, class_name='mt-2'),
                    ),
                ],
                body=True, class_name='mt-2'),
            html.Br(),
            dbc.Row(dbc.Col(id=self.ids.message), className='mt-12')

        ])

    def events(self):
        
        @callback(
            Output(self.ids.parent.store_filter_data, 'data'),
            Output(self.ids.parent.store_filter_data, 'clear_data'),
            Output(self.ids.message, 'children'),
            [
                Input(self.ids.btn_search, 'n_clicks'),
                Input(self.ids.btn_clear, 'n_clicks'),
            ],
            [
                State(self.ids.input_search, 'value'),
                State(self.componentCidade.ids.component_dropdown, 'value'),
                State(self.componentEstado.ids.component_dropdown, 'value'),
                State(self.ids.input_search, 'options'),
                State(self.componentCidade.ids.component_dropdown, 'options'),
                State(self.componentEstado.ids.component_dropdown, 'options'),
            ]
        )
        def search_data(btn, btn_clear, *args):
            if not btn and not btn_clear:
                raise PreventUpdate
            
            btn_ctx = ctx.triggered[0]["prop_id"].split(".")[0]
            
            
            if btn_ctx == self.ids.btn_clear:
                self.current_form = None
                return None, True, ''

            
            (
                text, muncipio_id, estado_id, options_text, options_municipio, options_estado
            ) = args

            try:
                self.current_form =  SessionForm(
                    estado_id=estado_id,
                    text=text,
                    municipio_id=muncipio_id
                )
                
                self.current_form.do_validator()
                
                
                self.current_form.municipio_label = ObjectUtil.get_selected_option_dropdown(muncipio_id, options_municipio)
                self.current_form.estado_label = ObjectUtil.get_selected_option_dropdown(estado_id, options_estado)
                self.current_form.text_label = ObjectUtil.get_selected_option_dropdown(text, options_text)

                
                return self.current_form.dict(), no_update, ''
                
            except Exception as ex:
                return no_update, no_update, dbc.Alert(str(ex), color='danger', duration=3000)
        
        @callback(
            Output(self.ids.input_search, 'options'),
            Input(self.ids.input_search, 'search_value')
        )      
        def search_text(value):
            if not value:
                raise PreventUpdate
            
            if len(value) < 3:
                return []

            data_filter = Cliente.search_filter(value)
            
            if len(data_filter):
                return [{'label': r.to_label, 'value': r.id} for r in data_filter]
            return []