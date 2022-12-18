from typing import List
from dash import html, dcc, callback, Input, Output, State, no_update, ctx, get_relative_path
from dash.exceptions import PreventUpdate
from pyapp.core.decorator import login_required
import dash_bootstrap_components as dbc
from .componentes.table_view import TableView
from .componentes.form import Form
from .componentes.filtro import Filtro
from .schema.ids import PageClienteIds, EnumTypeForm
from pyapp.core.pages.base import BasePage


@login_required
class Page(BasePage):

    def __init__(self) -> None:

        self.ids = PageClienteIds()
        
        self.componentFiltro = Filtro()
        
        self.componentTableView = TableView()
        
        
        self.componentForm = Form(EnumTypeForm.ADD)
        

        self.events()

    @property
    def template_path(self):
        return [
            get_relative_path('/clientes'), 
            get_relative_path('/clientes/{id:int}')
        ]

   
    @property
    def parent_layout(self):
        return 'LAYOUT_PAGE_APP'

    @property
    def access_control(self) -> List[str]:
        raise NotImplementedError
        # return ['admin']

    def __repr__(self) -> str:
        return 'Clientes Page'

    @property
    def title(self):
        return 'Clientes'

    @property
    def modal_cadastro(self):
        return html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle(
                            "Novo Cliente"), class_name='bg-success text-white'),
                        dbc.ModalBody(
                            html.Div(id=self.ids.modal_form_new_content))
                    ],
                    id=self.ids.modal_form_new,
                    size="xl",
                    backdrop='static',
                    is_open=False,
                ),
            ]
        )

    @property
    def modal_filtro(self):
        return html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle(
                            "Filtros"), class_name='bg-info text-white'),
                        dbc.ModalBody(id=self.ids.modal_filtro_content)
                    ],
                    id=self.ids.modal_filtro,
                    size="xl",
                    backdrop='static',
                    is_open=False,
                ),
            ]
        )

    def layout(self, *args, **kwargs):
        storage_state = html.Div(
            [
                dcc.Store(id=self.ids.store_filter_data, storage_type='session'),
                dcc.Store(id=self.ids.store_form_save_data),
                dcc.Store(id=self.ids.store_form_save_change_data),
                dcc.Store(id=self.ids.store_table_view_item_remove),
                dcc.Store(id=self.ids.store_table_view_page),
                dcc.Store(id=self.ids.store_filter_form_session)
            ]
        )

        cards_buttons = html.Div(
            [
                dbc.Card([
                    dbc.CardBody([
                        dbc.Button('Novo Cliente', color='success',
                                   class_name='me-2', id=self.ids.modal_form_new_btn_open),
                        dbc.Button(
                            "Filtros", color='info', class_name='position-relative me-2', id=self.ids.modal_filtro_btn_open),
                    ]),
                    dbc.CardFooter(id=self.ids.modal_filtro_badges_content)],
                    className="mb-3",
                )
            ]
        )

        content = html.Div(children=[
            storage_state,
            html.Button(id=self.ids.page_onload, style={'display': 'none'}),
            html.Br(),
            cards_buttons,
            self.breadcrumb,
            dbc.Row(
                dbc.Col(
                    [
                        self.modal_filtro,
                        self.modal_cadastro
                    ])
            ),
            dbc.Row([
                    dbc.Col(dbc.Alert("Clientes cadastrados", color='info'))
                    ]),
            html.Br(),
            self.componentTableView.layout()
        ])

        return content

    def events(self):
        
        
        @callback(
            Output(self.ids.modal_filtro_btn_open, 'children'),
            Output(self.ids.modal_filtro_badges_content, 'children'),
            Input(self.ids.store_filter_data, 'data'),
            Input(self.ids.page_onload, 'n_clicks'),
            State(self.ids.store_filter_data, 'data')
        )
        def filter_data(data, btn, data_state):
            text = 'Filtros'
            if data or data_state:
                
                data = data_state
                
                
                keys = list(filter(lambda key: str(key).endswith('_label'), data.keys()))
                
                badges = []
            
                
                for k in keys:
                    value = data.get(k)
                    
                    if isinstance(value, list) and len(value):
                        badges.append(dbc.Badge(value[0].get('label'), pill=True, color="secondary", className="me-1"))
                        
                span_badges = html.Span()
                
                if len(badges):
                    span_badges = html.Span(badges)
                    
                span_pill = html.Span(
                    [
                        text,
                        dbc.Badge(
                            f'{len(badges)}+',
                            color="danger",
                            pill=True,
                            text_color="white",
                            className="position-absolute top-0 start-100 translate-middle",
                        )
                    ]
                )
                    
                
                return span_pill, span_badges
                    
                
            else:
                return text, ''

        @callback(
            [
                Output(self.ids.modal_filtro, 'is_open'),
                Output(self.ids.modal_form_new, 'is_open'),
                Output(self.ids.modal_form_new_content, 'children'),
                Output(self.ids.modal_filtro_content, 'children'),

            ],
            [
                Input(self.ids.modal_filtro_btn_open, 'n_clicks'),
                Input(self.ids.modal_form_new_btn_open, 'n_clicks'),
            ],
            [
                State(self.ids.modal_filtro, 'is_open'),
                State(self.ids.modal_form_new, 'is_open'),
                State(self.ids.store_filter_data, 'data')
            ]
        )
        def bnt_trigger(modal_filtro_btn_open, modal_form_new_btn_open, *args):

            if not modal_filtro_btn_open and not modal_form_new_btn_open:
                raise PreventUpdate

            (
                is_modal_filtro,
                is_modal_cadastro,
                current_form_filtro
            ) = args

            btn_id = ctx.triggered[0]["prop_id"].split(".")[0]
            
            if btn_id == self.ids.modal_filtro_btn_open:
                return [not is_modal_filtro, False, no_update, self.componentFiltro.layout(current_form_filtro)]
                

            try:
                return [False, not is_modal_cadastro, self.componentForm.layout(), no_update]
            except Exception as err:
                raise PreventUpdate