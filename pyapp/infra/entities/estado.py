from sqlalchemy_serializer import SerializerMixin
from pyapp.ext.database import db


class Estado(db.Model, SerializerMixin):
    """
        Estado Entity
    """
    __tablename__ = 'estados'
    
    id = db.Column(db.Integer, primary_key=True, index=True, nullable=False)
    sigla = db.Column(db.String(5))
    nome = db.Column(db.String(150))