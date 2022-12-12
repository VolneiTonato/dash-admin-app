import dash_bootstrap_components as dbc
from dash import html
from flask_sqlalchemy.pagination import Pagination
import polars as pl
from typing import Literal,  Union
from pyapp.utils.generic_util import ObjectUtil

class DinamicTableBootstrapUtil:
    
    _table_header = None
    _table_rows = []
    
    def __init__(self) -> None:
        self._table_rows = []
    

    def compile(self):
        return dbc.Table([
                self._table_header, 
                html.Tbody(self._table_rows)
            ], bordered=False
        )
    
    def add_button(self, id_component, idx, value, ctype: Literal['delete', 'edit', 'pdf','table']):
        id = {
            'type' : id_component,
            'index': idx
        }
        
        obj = {}
        
        if ctype == 'delete':
            obj.update({'class' : 'bi-trash', 'color': 'danger'})
        elif ctype == 'edit':
            obj.update({'class' : 'bi-pencil', 'color': 'success'})
        elif ctype == 'pdf':
            obj.update({'class' : 'bi-filetype-pdf', 'color': 'info'})
        elif ctype == 'table':
            obj.update({'class' : 'bi-table', 'color': 'secondary'})
        else:
            raise Exception('Button invalid!')
            
        
        return dbc.Button([html.I(className=f'bi {obj["class"]}')], className="me-1", color=obj['color'], value=value, id=id, n_clicks=0)
    
    
    def add_rows_to_dict(self, rows: tuple):
        self._table_rows.append([html.Td(c) for c in rows])
        return self
        
    
    def add_header_to_columns(self, columns):
        cols_th = [html.Th(c) for c in columns]
        self._table_header = html.Thead([html.Tr(cols_th)])
        return self
    
    
    
    def create_table(self, model: Pagination, columns:list, title_case:bool = False):
        
        paginas = []

        content = {}
    
        for c in columns:
            if isinstance(c, str):
                c_name = c
                if title_case:
                    c_name = c.title()
                content[c_name] = str(ObjectUtil.getattr_model(model, c, default=''))
            elif isinstance(c, dict):
                column_name, path_object = next(iter(c.items()))
                content[column_name] = str(ObjectUtil.getattr_model(model, path_object, default=''))
            
        paginas.append(content)
        

        df = pl.DataFrame(paginas)
        
        self.add_header_to_columns(df.columns)

        for row in df.rows():
            self.add_rows_to_dict(row)
            
        if len(self._table_rows):
            for i, element in enumerate(self._table_rows):
                self._table_rows[i] = html.Tr(element)
                

        return self.compile()
    
    def create_table_to_pagination(self, 
                                   model:Pagination, 
                                   columns:list=[], 
                                   key:Union[dict, str, None]=None,
                                   id_btn_edit:str=None,
                                   id_btn_remove:str=None,
                                   id_btn_view_pdf:str=None,
                                   id_btn_view_table:str=None,
                                   title_case:bool = False):
        
        
        paginas = []
        struct_columns_df = []
        
        current_key = ''
        
        for obj_model in model.items:
            content = {}
        
            for c in columns:
                if isinstance(c, str):
                    c_name = c
                    if title_case:
                        c_name = c.title()
                    content[c_name] = str(ObjectUtil.getattr_model(obj_model, c, default=''))
                elif isinstance(c, dict):
                    column_name, path_object = next(iter(c.items()))
                    content[column_name] = str(ObjectUtil.getattr_model(obj_model, path_object, default=''))
                    
            if len(struct_columns_df) == 0:
                struct_columns_df = list(content.keys()) 
                    
            if isinstance(key, dict):
                column_name, path_object = next(iter(key.items()))
                content[column_name] = str(ObjectUtil.getattr_model(obj_model, path_object, default=''))
                current_key = column_name
            elif key:
                content[key] = str(ObjectUtil.getattr_model(obj_model, key, default=''))
                current_key = key
                
            paginas.append(content)
        

        df = pl.DataFrame(paginas)
    

        if len(struct_columns_df):
            df_copy = df.select(struct_columns_df)
            
            
        self.add_header_to_columns(df_copy.columns)
        
        for row in df_copy.rows():
            self.add_rows_to_dict(row)
            
            
        if len(self._table_rows):
            
            if current_key:
                
                keys = [c[current_key] for c in df.select(current_key).to_dicts()]

                for i, element in enumerate(self._table_rows):

                    buttons = []
                    
                    if id_btn_edit:
                        buttons.append(self.add_button(id_btn_edit, i,  keys[i], ctype='edit'))
                        
                    if id_btn_remove:
                        buttons.append(self.add_button(id_btn_remove, i, keys[i], ctype='delete'))
                        
                    if id_btn_view_pdf:
                        buttons.append(self.add_button(id_btn_view_pdf, i, keys[i], ctype='pdf'))
                        
                    if id_btn_view_table:
                        buttons.append(self.add_button(id_btn_view_table, i, keys[i], ctype='table'))
 
                    if len(buttons):
                        element.append(html.Div(buttons))
                        self._table_rows[i] = element
                        
            for i, element in enumerate(self._table_rows):
                self._table_rows[i] = html.Tr(element)
                

        return self.compile()
    