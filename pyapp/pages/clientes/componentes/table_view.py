from dash import html, dcc, Output, Input, State, callback, ctx, ALL, no_update
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from pyapp.infra.schemas.cliente import ClienteFilterDTO
from pyapp.utils.dinamic_table_bootstrap_util import DinamicTableBootstrapUtil
from pyapp.infra.entities.cliente import Cliente
from .form import Form
from pyapp.pages.clientes.schema.ids import (
    TableViewComponentClienteIds,
    EnumTypeForm
)


class TableView:

    ids: TableViewComponentClienteIds = None

    def __init__(self) -> None:

        self.ids = TableViewComponentClienteIds()

        self.componentForm = Form(ctype=EnumTypeForm.EDIT)
    

        self.events()

    @property
    def modal_edicao(self):
        return html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle(
                            "Edição de cadastro"), class_name='bg-success text-white'),
                        dbc.ModalBody(
                            html.Div(id=self.ids.modal_form_edit_content))
                    ],
                    id=self.ids.modal_form_edit,
                    size="xl",
                    backdrop='static',
                    is_open=False,
                ),
            ]
        )

    @property
    def modal_delete(self):
        return html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalBody(
                            [
                                dbc.Alert(
                                    [
                                        html.H2([
                                            html.Span(
                                                "Deseja remover o cliente "),
                                            html.Span(
                                                id=self.ids.modal_question_item_selected, className="alert-link"),
                                            html.Span(" ?"),

                                        ]),
                                    ],
                                    color="info",
                                ),
                            ]

                        ),
                        dbc.ModalFooter(
                            [
                                dbc.Button(
                                    "Sim", color='success', class_name='me-1', id=self.ids.modal_question_btn_confirm),
                                dbc.Button(
                                    "Não", color='danger', class_name='me-1', id=self.ids.modal_question_btn_close),

                            ]
                        ),
                    ],
                    id=self.ids.modal_question,
                    size="lg",
                    backdrop='static',
                    centered=True,
                    is_open=False,
                ),
            ]
        )

    def layout(self):
        return html.Div([
            dbc.Row(
                dbc.Col([
                    html.Div([
                        dbc.Button(
                            [
                                html.I(className='bi bi-arrow-clockwise')
                            ],
                            id=self.ids.onload_component,
                            color='success')
                    ]
                    )
                ])
            ),
            self.modal_edicao,
            self.modal_delete,
            dcc.Loading([
                html.Div(id=self.ids.content_component),
            ], id=self.ids.loading_component)
        ])

    def events(self):

        @callback(
            [
                Output(self.ids.modal_form_edit, 'is_open'),
                Output(self.ids.modal_form_edit_content, 'children')
            ],
            Input({'type': self.ids.table_btn_edit, 'index': ALL}, 'n_clicks'),
            State({'type': self.ids.table_btn_edit, 'index': ALL}, 'value')

        )
        def handle_edit_form(btn_click, value):

            if not btn_click or len(ctx.triggered) != 1:
                raise PreventUpdate

            try:
                n_click = ctx.triggered[0]["value"] or 0

                if n_click > 0:
                    idx = ctx.triggered_id['index']

                    id = value[idx]

                    model = Cliente.query.get(f'{id}')

                    return True, self.componentForm.layout(data=model)

                raise PreventUpdate
            except:
                raise PreventUpdate

        @callback(
            [
                Output(self.ids.modal_question, 'is_open'),
                Output(self.ids.modal_question_item_selected, 'children'),
                Output(self.ids.parent.store_table_view_item_remove, 'data'),
            ],
            [
                Input({'type': self.ids.table_btn_remove,
                      'index': ALL}, 'n_clicks'),
                Input(self.ids.modal_question_btn_confirm, 'n_clicks'),
                Input(self.ids.modal_question_btn_close, 'n_clicks')
            ],
            [
                State({'type': self.ids.table_btn_remove, 'index': ALL}, 'value'),
                State(self.ids.parent.store_table_view_item_remove, 'data')
            ]


        )
        def display_remove(*args):
            (
                btn_click,
                btn_confirm_delete,
                btn_close_delete,
                state_value_trash,
                state_value_id_trash
            ) = args

            btn_ctx = ctx.triggered[0]["prop_id"].split(".")[0]


            if btn_ctx == self.ids.modal_question_btn_confirm and state_value_id_trash:
                Cliente.remove(state_value_id_trash)
                return False, '', 'REMOVED_SESSION'

            if btn_ctx == self.ids.modal_question_btn_close and state_value_id_trash:
                return False, '', no_update

            try:

                n_click = ctx.triggered[0]["value"] or 0

                if n_click > 0:
                    idx = ctx.triggered_id['index']

                    id = state_value_trash[idx]

                    model = Cliente.query.get(f'{id}')
                    
                    return True, model.razao_social, str(model.id)

                raise PreventUpdate

            except:
                raise PreventUpdate

        @callback(
            Output(self.ids.parent.store_table_view_page, 'data'),
            Input(self.ids.table_pagination, 'active_page')
        )
        def paginator(page):
            if page:
                return page
            return 0

        def refresh_table(data, page):

            try:
                if len(data.items):

                    table = DinamicTableBootstrapUtil().create_table_to_pagination(data, columns=[
                        {'Razão Social': 'razao_social'},
                        'fantasia',
                        'logradouro',
                        'email',
                        'cep',
                        {'município': 'municipio.nome'},
                        {'UF': 'municipio.estado.sigla'}
                    ], id_btn_edit=self.ids.table_btn_edit,
                        id_btn_remove=self.ids.table_btn_remove,
                        key={'id': 'id'}, title_case=True)

                    paginator = dbc.Pagination(id=self.ids.table_pagination,
                                               first_last=True,
                                               previous_next=True,
                                               active_page=1 if page == 0 else page,
                                               max_value=data.pages,
                                               fully_expanded=False)

                    return html.Div([table, paginator])
                raise Exception
            except:
                
                return dbc.Row(dbc.Col(dbc.Alert(html.H4('*** Nenhum cliente encontrado'), color='warning'), lg=12), class_name='mt-2' ,justify='center')

        @callback(
            [
                Output(self.ids.loading_component, 'loading_state'),
                Output(self.ids.content_component, 'children')
            ],
            [
                Input(self.ids.onload_component, 'n_clicks'),
                Input(self.ids.parent.store_table_view_page, 'data'),
                Input(self.ids.parent.store_filter_data, 'data'),
                Input(self.ids.parent.store_form_save_data, 'data'),
                Input(self.ids.parent.store_form_save_change_data, 'data'),
                Input(self.ids.parent.store_table_view_item_remove, 'data')
            ]
        )
        def load_component(*args):

            (
                onload,
                store_page,
                store_filter,
                store_form_save,
                store_form_save_change,
                store_table_item_remove
            ) = args

            if not store_page:
                store_page = 0

            component_ctx = ctx.triggered[0]["prop_id"].split(".")[0]

            if component_ctx == self.ids.parent.store_table_view_item_remove:
                if store_table_item_remove == 'REMOVED_SESSION':
                    store_page = 0
                else:
                    raise PreventUpdate

            if component_ctx == self.ids.parent.store_filter_data:
                store_page = 0

            clientes = []

            if store_filter:
                store_filter = ClienteFilterDTO(**store_filter)
                clientes = Cliente.find_by_filter_paginator(
                    store_filter, store_page)

            else:
                clientes = Cliente.find_all_paginator(store_page)

            component_table = refresh_table(clientes, store_page)

            return {},  component_table
