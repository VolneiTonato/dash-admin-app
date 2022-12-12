from sqlalchemy_serializer import SerializerMixin
from pyapp.ext.database import db
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from pyapp.utils.generic_util import ObjectUtil
from pyapp.infra.repositories import paginator
from .municipio import Municipio
from faker import Faker
from .estado import Estado
from pyapp.infra.schemas.cliente import (
    ClienteSaveDTO,
    ClienteMergeDTO,
    ClienteFilterDTO
)
from sqlalchemy.exc import SQLAlchemyError

class Cliente(db.Model, SerializerMixin):
    """
        Cliente Entity
    """
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True, index=True, nullable=False)
    email = db.Column(db.String(100))
    logradouro = db.Column(db.String(150))
    bairro = db.Column(db.String(50))
    cnpj = db.Column(db.String(18))
    telefone = db.Column(db.String(20))
    cep = db.Column(db.String(20))
    razao_social = db.Column(db.String(100), nullable=False)
    fantasia = db.Column(db.String(100))
    municipio_id = db.Column(db.Integer, db.ForeignKey(Municipio.id))
    created_at = db.Column(DateTime(timezone=True), default=func.now())
    updated_at = db.Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    municipio = db.relationship(Municipio, innerjoin=True)
    
    @property
    def to_label(self):
        return f"""
            {self.razao_social} {self.fantasia} | 
            {self.email} | Fone: {self.telefone} | 
            {ObjectUtil.getattr_model(self.municipio, 'estado.sigla', '')} -
            {ObjectUtil.getattr_model(self.municipio, 'nome', '')} 
        """.strip('\n')
    
    
    @classmethod
    def find_all_paginator(cls, page=0):
        return paginator(db.select(cls).order_by(cls.updated_at.desc()), current_page=page)
    
    
    @classmethod
    def find_by_filter_paginator(cls, data: ClienteFilterDTO, page=0):
        
        
        query = db.session.query(cls)
        
        if data.text:
            query = query.filter(cls.id == f'{data.text}')
            
        if data.municipio_id:
            query = query.filter(cls.municipio_id == data.municipio_id)
            
        if data.estado_id and not data.municipio_id:
            query = query.join(Municipio).join(Estado, Municipio.estado_id == Estado.id)\
                .filter(Estado.id == data.estado_id)


        return paginator(query, current_page=page)
    

    @classmethod
    def search_filter(cls, text: str):
        try:
            data = db.session.query(cls)\
                .filter(
                    (cls.razao_social.ilike(f'%{text}%')) | (cls.fantasia.ilike(f'%{text}%')) \
                    | (cls.logradouro.ilike(f'%{text}%')) \
                    | (cls.bairro.ilike(f'%{text}%')) \
                    | (cls.telefone.ilike(f'%{text}%'))
                ).limit(20).all()
            return data
        except Exception as ex:
            return SQLAlchemyError(ex)
    
    @classmethod
    def remove(cls, id: str):
        try:
            obj = cls.query.get(f'{id}')
            db.session.delete(obj)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            raise SQLAlchemyError(ex)
    
    @classmethod
    def save(cls, data:ClienteSaveDTO):
        try:
            obj = cls(**data.dict())
            db.session.add(obj)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            raise SQLAlchemyError(ex)
    
    @classmethod
    def update(cls, data:ClienteMergeDTO):
        try:
            obj = cls(**data.dict())
            db.session.merge(obj)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            raise SQLAlchemyError(ex)