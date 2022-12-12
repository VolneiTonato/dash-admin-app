from typing import List
from dash import html
import dash_bootstrap_components as dbc
from pyapp.core.decorator import login_required
from hashlib import md5

@login_required
class Page:
    
    def __init__(self) -> None:
        self.aio_id = md5(__name__.encode()).hexdigest()
    
    @property
    def template_path(self):
        return ['/']
    
    @property
    def path(self):
        return '/'
    
    @property
    def parent_layout(self):
        return 'LAYOUT_PAGE_APP'
    
    @property
    def access_control(self) -> List[str]:
        return ['admin']
    
    def __repr__(self) -> str:
        return 'Home Page'

    @property
    def title(self):
        return 'Home Page'
    
    
    
    def _create_card(self, header, title, text, footer):
        return dbc.Card(
            [
                dbc.CardHeader(header),
                dbc.CardBody(
                    [
                        html.H4(title, className="card-title"),
                        html.P(text, className="card-text"),
                    ]
                ),
                dbc.CardFooter(footer),
            ],
            style={"width": "18rem"},
        )
    
    
    def layout(self, *args, **kwargs):
        
        
        layout = html.Div([
            dbc.Row([dbc.Col(
                self._create_card('header', 'title', 'this is some card text', 'this is the footer'), 
                width=3, class_name='mt-5'
            )]*10)
        ])
        
        return layout