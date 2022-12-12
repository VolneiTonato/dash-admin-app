from datetime import timedelta
from flask import Flask
from pyapp.ext import setup_ext
from pyapp.ext.dash import dash_app
import redis
from pyapp.config import get_settings
import argparse

def create_flask_app():
    settings = get_settings()
    
    server = Flask(__name__)                 
    
    server.config.update(SECRET_KEY=settings.secret_session)
    server.config['SESSION_TYPE'] = "redis"
    server.config['SESSION_REDIS'] = redis.from_url(f'{settings.redis_db}/1')
    server.config['SESSION_PERMANENT'] = False
    server.config['SESSION_USE_SIGNER'] = True
    server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
    
    server.config['CACHE_TYPE'] = 'redis'
    server.config['CACHE_REDIS_URL'] = f'{settings.redis_db}/2'
    
    server.config['SQLALCHEMY_ECHO'] = False
    
    server.config['SQLALCHEMY_DATABASE_URI'] = settings.sqlalchemy_database_uri
    
    return server

def create_app(args_command=None):
    
    app = create_flask_app()   

    
    setup_ext.load_extensions(app)
    
    setup_ext.load_entities(app, args_command)

    
    with  app.app_context() as ctx:
        dash_app.run(debug=True)
        
    
    

if __name__ == '__main__':
    
    parse = argparse.ArgumentParser()
    parse.add_argument('--command', required=False)
    args = parse.parse_args()

    create_app(args)