from flask import Flask
from datetime import timedelta
import redis
from pyapp.ext import setup_ext
from pyapp.ext.dash import dash_app
from pyapp.config import get_settings

def create_flask_app():
    
    settings = get_settings()
    
    server = Flask(__name__)                 
    
    server.config.update(SECRET_KEY=settings.SECRET_SESSION)
    server.config['SESSION_TYPE'] = "redis"
    server.config['SESSION_REDIS'] = redis.from_url(f'{settings.REDIS_HOST}/1')
    server.config['SESSION_PERMANENT'] = False
    server.config['SESSION_USE_SIGNER'] = True
    server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
    
    server.config['CACHE_TYPE'] = 'redis'
    server.config['CACHE_REDIS_URL'] = f'{settings.REDIS_HOST}/2'
    
    server.config['SQLALCHEMY_ECHO'] = False
    
    server.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    
    return server

def create_app(args_command=None):
    
    app = create_flask_app()   

    setup_ext.load_extensions(app)
    
    setup_ext.load_entities(app, args_command)
    
    return app

def run_dash(args):
    app = create_app(args)

    dash_app.run(debug=True, host='0.0.0.0')