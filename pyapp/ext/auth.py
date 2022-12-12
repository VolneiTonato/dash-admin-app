from flask_login import login_user, LoginManager, UserMixin
from pyapp.guard.auth_guard_user_ldap import AuthGuardUserLdap


login_manager = LoginManager()
login_manager.login_view = '/login'

def login(username, password):
    if username == 'administrator' and password == '123':
        return login_user(AuthGuardUserLdap(username))    
    
    return False


def init_app(app):
    
    @login_manager.user_loader
    def load_user(username):
        return AuthGuardUserLdap(username)
    
    login_manager.init_app(app)