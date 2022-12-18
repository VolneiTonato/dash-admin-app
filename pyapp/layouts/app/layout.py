from dash import html, callback, Output, Input, State, get_relative_path
import dash_bootstrap_components as dbc
from dash.development.base_component import Component
from pyapp.config import themes
from pyapp.utils.styled_components_util import StyleComponentUtil
from pyapp.ext.cache import cache
from hashlib import md5
from pyapp.core.pages.base import BaseIds

class LayoutPage:
    
    class Ids(BaseIds):
        
        sidebar: str
        main: str
        sidebar_toggle: str
        collapse: str
        navbar_toggle: str
        content: str
        
        
        def __init__(self, aio_id, root) -> None:
            super().__init__(aio_id, root)


    ids : Ids = None
    
    def __init__(self, aio_id='layout-app'):
        
        self.aio_id = md5(aio_id.encode()).hexdigest()
        
        self.ids = LayoutPage.Ids(aio_id=self.aio_id, root='LayoutAppIAO')
        
        self.events()
        
    def __repr__(self) -> str:
        return 'LAYOUT_PAGE_APP'
    
    @cache.memoize(timeout=60*10)
    def load_data(self):
        style = StyleComponentUtil()
        style.add_file_external(themes.BOOTSTRAP)
        style.add_file_external(dbc.icons.BOOTSTRAP)
        style.add_file_scss(
            'style.scss', 
            folder_file=__file__,
            is_base64=True,
            **{
                '#sidebar' : f'#{self.ids.sidebar}',
                '#collapse': f'#{self.ids.collapse}',
                '#navbar-toggle' : f'#{self.ids.navbar_toggle}',
                '#sidebar-toggle' : f'#{self.ids.sidebar_toggle}',
                '#main' : f'#{self.ids.main}',
                '#content' : f'#{self.ids.content}'
            }
            )
        self.style = style.link_css

    
    @property
    @cache.memoize(60*2)
    def navbar(self):
        return dbc.NavbarSimple(
                children=[
                    dbc.Collapse(
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True,
                    ),
                    dbc.NavItem(dbc.NavLink("sair", href=get_relative_path('/logout'))),
                ],
                color="primary",
                class_name='navbar-custom',
                dark=True
                

            )
    
    @property
    def sidebar(self):
        
        sidebar_header = dbc.Row(
            [
                dbc.Col(html.H2("App", className="display-4")),
                dbc.Col(
                    [
                        html.Button(
                            html.Span(className="navbar-toggler-icon"),
                            className="navbar-toggler",
                            style={
                                "color": "rgba(0,0,0,.5)",
                                "border-color": "rgba(0,0,0,.1)",
                            },
                            id=self.ids.navbar_toggle,
                        ),
                        html.Button(
                            html.Span(className="navbar-toggler-icon"),
                            className="navbar-toggler",
                            style={
                                "color": "rgba(0,0,0,.5)",
                                "border-color": "rgba(0,0,0,.1)",
                            },
                            id=self.ids.sidebar_toggle,
                        ),
                    ],
                    width="auto",
                    align="center",
                ),
            ]
        )

        return html.Div(
            [
                sidebar_header,
                html.Div(
                    [
                        html.Hr(),
                        html.P(
                            "Dash Admin App "
                            "",
                            className="lead",
                        ),
                    ],
                    id="blurb",
                ),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavLink("Home", href=get_relative_path("/"), active="exact"),
                            dbc.NavLink("Clientes", href=get_relative_path("/clientes"), active="partial")
                        ],
                        vertical=True,
                        pills=True,
                    ),
                    id=self.ids.collapse,
                ),
            ],
            id=self.ids.sidebar,
        )
        

    def layout(self, children:Component):
        self.load_data()
        
        
        content = dbc.Container(children, id=self.ids.content, fluid=True)
        
        
        return html.Div([self.style, self.sidebar, html.Div([self.navbar, content], id=self.ids.main)])
        
        
        
        
    def events(self):
        @callback(
            [
                Output(self.ids.sidebar, "className"),
                Output(self.ids.main, "className")
            ],
            [Input(self.ids.sidebar_toggle, "n_clicks")],
            [State(self.ids.sidebar, "className")],
        )
        def toggle_classname(n, classname):
            collapsed = ''
            if n and classname == "":
                collapsed = "collapsed"

            return [collapsed]*2


        @callback(
            Output(self.ids.collapse, "is_open"),
            [Input(self.ids.navbar_toggle, "n_clicks")],
            [State(self.ids.collapse, "is_open")],
        )
        def toggle_collapse(n, is_open):
            if n:
                return not is_open
            return is_open


