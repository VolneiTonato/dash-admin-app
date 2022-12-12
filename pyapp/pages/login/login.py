from dash import html, callback, Output, State, Input, dcc, no_update
from dash.exceptions import PreventUpdate
from pyapp.utils.styled_components_util import StyleComponentUtil
import dash_bootstrap_components as dbc
from pyapp.config import themes
from .schema.ids import PageLoginIds
from pyapp.ext.auth import login


class Page:

    ids: PageLoginIds = None

    def __init__(self) -> None:
        self.ids = PageLoginIds()
        self.events()

    @property
    def path(self):
        return '/login'

    @property
    def title(self):
        return 'Login Page'

    def load_data(self):
        style = StyleComponentUtil()
        style.add_file_external(themes.BOOTSTRAP)
        style.add_file_external(dbc.icons.BOOTSTRAP)

        style.add_file_scss(
            'style.scss', folder_file=__file__, is_base64=True)
        style.add_file_external(themes.FONTAWESOME_5)

        self.StyleComponent = style.link_css

    def layout(self, *args, **kwargs):
        self.load_data()

        return html.Div([
            self.StyleComponent,
            dcc.Location(id=self.ids.page_url_refresh, refresh=True),

            dbc.Container(
                [
                        dbc.Row(
                            [
                                dbc.Col(lg=3, md=2),
                                dbc.Col(
                                    [
                                        dbc.Col(html.I(className='fa fa-key'),
                                                lg=12, class_name='login-key'),
                                        dbc.Col('ADMIN PANEL',
                                                class_name='login-title'),

                                        dbc.Col(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Form(
                                                            [
                                                                html.Div(
                                                                    [
                                                                        html.Label('USERNAME', className='form-control-label'),
                                                                        dcc.Input(id=self.ids.input_username, className='form-control')
                                                                    ],
                                                                    className='form-group'
                                                                ),
                                                                html.Div(
                                                                    [
                                                                        html.Label('PASSWORD', className='form-control-label'),
                                                                        dcc.Input(type='password', id=self.ids.input_password, className='form-control')
                                                                    ],
                                                                    className='form-group'
                                                                ),

                                                                dbc.Col(
                                                                    [
                                                                        dbc.Col(id=self.ids.message, lg=12, class_name='login-btm login-text'),
                                                                        html.Br(),
                                                                        dbc.Col(
                                                                            [
                                                                                dcc.Loading(
                                                                                    html.Button('LOGIN', id=self.ids.page_btn_login, type='button', className='btn btn-outline-primary'),
                                                                                    id=self.ids.page_loading_login
                                                                                )
                                                                            ], lg=12, class_name='login-btm login-button'),


                                                                    ], lg=12, class_name='loginbttm'
                                                                )


                                                            ]
                                                        )
                                                    ],
                                                    lg=12, class_name='login-form'
                                                )
                                            ], lg=12, class_name='login-form'
                                        ),
                                        dbc.Col(lg=3, md=2)
                                    ],
                                    lg=6, md=8, class_name='login-box')
                            ]
                        )
                        ], fluid=False
            )

        ])

    def events(self):

        @callback(
            Output(self.ids.page_url_refresh, 'pathname'),
            Output(self.ids.page_loading_login, 'loading_state'),
            Output(self.ids.message, 'children'),
            Output(self.ids.message, 'style'),
            Input(self.ids.page_btn_login, 'n_clicks'),
            State(self.ids.input_username, 'value'),
            State(self.ids.input_password, 'value')
        )
        def process_login(btn, input_username, input_password):
            if not btn:
                raise PreventUpdate

            try:

                if input_username and input_password:

                    try:
                        is_auth = login(input_username, input_password)
                        if not is_auth:
                            raise Exception('Erro ao autenticar')

                        return '/', {}, '', {}
                    except Exception as ex:
                        raise Exception(ex)

                raise Exception('Usuário/senha obrigatórios!')
            except Exception as ex:
                return no_update, {}, str(ex), {'display': 'block'}
