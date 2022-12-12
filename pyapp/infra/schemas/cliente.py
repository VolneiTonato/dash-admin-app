from pyapp.config import BaseModel
from pydantic import validator, constr
from typing import Optional
from pyapp.utils.generic_util import StringUtil
import re
from uuid import UUID

class ClienteRemoveDTO(BaseModel):
    id: UUID


class ClienteFilterDTO(BaseModel):
    text: Optional[str]
    municipio_id: Optional[str]
    estado_id : Optional[str]
    
    
    
    def do_validator(self):
        values = []
        for property in self.__annotations__:
            values.append(getattr(self, property))
            
        if len(list(filter(lambda row : row, values))) > 0:
            return True
        raise Exception('informe algum valor')
    
    


class ClienteSaveDTO(BaseModel):
    razao_social: constr(to_upper=True, strict=True, strip_whitespace=True)
    fantasia: Optional[constr(to_upper=True, strict=True, strip_whitespace=True)]
    bairro: Optional[constr(to_upper=True, strict=True, strip_whitespace=True)]
    email: Optional[str]
    cep: Optional[str]
    municipio_id: Optional[str]
    cnpj: str
    telefone: Optional[str]
    logradouro: Optional[constr(to_upper=True, strict=True, strip_whitespace=True)]
    
    
    @validator('email')
    def do_email(cls, value):
        
        if value:
            pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            
            if re.match(pattern, value):
                return value
            raise ValueError('Email inválido!')
        
        return value
        
    
    
    @validator('razao_social')
    def do_nome(cls, value):
        if not value or value.strip() == '':
            raise ValueError('Razão Social obrigatório!')
        return value
    
    @validator('cep')
    def do_cep(cls, value):
        
        if value:
            
            try:
            
                v = StringUtil.to_number(value)
                
                if len(v) == 8:
                    return value
                elif len(v) > 0:
                    raise ValueError('CEP inválido!')
            except:
                pass
        return ''
    
    @validator('telefone')
    def do_telefone(cls, value):
        v = StringUtil.to_number(value)
        if v:
            if v[0] == '0':
                v = v[1:]

            if len(v) == 11:
                return value
            elif len(v) > 0:
                raise ValueError('Telefone inválido!')
        return ''


class ClienteMergeDTO(ClienteSaveDTO):
    id: str
    
    
    @validator('id')
    def do_id(cls, value):
        try:
            return int(value)
        except ValueError:
            raise ValueError('id inválido')
        