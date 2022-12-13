from dash import Dash
from flask import Flask
from pyapp.routers.router_dash import init_app as init_app_router, page_container, get_layout

dash_app = Dash(
    title='App Dash',
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
    serve_locally=True,
    assets_folder='assets',
    update_title='carregando...',
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    url_base_pathname='/'
)

def init_app(app: Flask):

    dash_app.init_app(app)

    init_app_router(app, dash_app)
    
    dash_app.layout = page_container
