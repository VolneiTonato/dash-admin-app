from sqlalchemy_serializer import SerializerMixin
from pyapp.ext.database import db
from .estado import Estado


class Municipio(db.Model, SerializerMixin):
    """
        Municipio Entity
    """
    __tablename__ = 'municipios'
    
    id = db.Column(db.Integer, primary_key=True, index=True, nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey(Estado.id), nullable=False)
    nome = db.Column(db.String(150))
    
    estado = db.relationship(Estado, innerjoin=True)
    
    @classmethod
    def find_by_estado(cls, estado_id):
        return cls.query.filter_by(estado_id=estado_id)