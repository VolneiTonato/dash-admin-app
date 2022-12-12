from flask_login import UserMixin
from flask import session
from dataclasses import dataclass
from pyapp.utils.session_util import SessionUtil

@dataclass
class AuthGuardUserLdap(UserMixin):
    def __init__(self, username):
        self.id = username