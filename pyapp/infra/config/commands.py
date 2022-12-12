from pyapp.ext.database import db
from sqlalchemy import Integer
import pandas as  pd
from pyapp.infra.entities.cliente import Cliente
from pyapp.infra.schemas.cliente import ClienteSaveDTO
from faker import Faker

def populate_clientes_database():
    
    faker = Faker(locale='pt_BR')
    for _ in range(100):
        try:
            cliente_schema = ClienteSaveDTO(
                email=faker.company_email(),
                logradouro=faker.street_name(),
                bairro=faker.bairro(),
                latitude=faker.latitude(),
                longitude=faker.longitude(),
                cnpj=faker.cnpj(),
                cep=faker.postcode(),
                telefone=faker.cellphone_number()[4:],
                razao_social=faker.name(),
                fantasia=faker.company(),
            )
            
            cliente = Cliente(**cliente_schema.dict())
            try:
                db.session.add(cliente)
                db.session.commit()
            except:
                db.session.rollback()  
        except:
            pass  

        

def populate_estados_database():
    with db.engine.begin() as t:
        df = pd.read_json('pyapp/infra/data/imports/estados.json')
        df = df.drop_duplicates(subset=['sigla'])
        df.to_sql('estados', con=t, index=False, if_exists='append',dtype={'id': Integer()})
    
        
def populate_municipios_database():
    with db.engine.begin() as t:
        df = pd.read_json('pyapp/infra/data/imports/municipios.json')
        df.to_sql('municipios', con=t, index=False, if_exists='append', dtype={'id': Integer(), 'estado_id': Integer()})