from flask import session

class SessionUtil:
    
    def registry(name , value):
        session[name] = value
        
    def get_session(name):
        if session.get(name):
            return session[name]
        return None
    
    def is_session(name):
        return SessionUtil.get_session(name) != None
        
        