from pyapp.core.pages.base import BaseIds
from hashlib import md5
from enum import Enum

class EnumTypeForm(Enum):
    EDIT='edit'
    ADD='add'


class PageClienteIds(BaseIds):
    
    store_form_save_data: str
    store_form_save_change_data: str
    store_table_view_page: str
    store_table_view_item_remove: str
    store_filter_data: str
    store_filter_form_session: str
    
    
    modal_filtro: str
    modal_filtro_content: str
    modal_filtro_btn_open: str
    modal_filtro_btn_close: str
    modal_filtro_btn_confirm: str
    modal_filtro_btn_search: str
    modal_filtro_badges_content: str
    
    modal_form_new:str 
    modal_form_new_content: str
    modal_form_new_btn_open: str
    
    
    page_onload: str

    
    def __init__(self) -> None:
        aio_id = md5(f'{__name__}-{str(PageClienteIds.__name__)}'.encode()).hexdigest()
        super().__init__(aio_id, root='PageClienteAIO')
        
        
class TableViewComponentClienteIds(BaseIds):
    
    modal_form_edit: str
    modal_form_edit_content: str
    modal_form_edit_btn_open: str
    
    modal_question: str
    modal_question_content: str
    modal_question_btn_confirm: str
    modal_question_btn_close: str
    modal_question_item_selected: str
    
    onload_component: str
    
    content_component: str
    loading_component: str
    
    table_pagination: str
    table_btn_edit: str
    table_btn_remove: str

    
    def __init__(self) -> None:
        aio_id = md5(f'{__name__}-{str(PageClienteIds.__name__)}'.encode()).hexdigest()
        self.parent = PageClienteIds()
        super().__init__(aio_id, root='ComponentTableViewClienteIAO')   
        

class FitroComponentClienteIds(BaseIds):
    input_search: str
    btn_search: str
    btn_clear: str
    message: str
    
    onload_component: str

    
    def __init__(self) -> None:
        aio_id = md5(f'{__name__}-{str(FitroComponentClienteIds.__name__)}'.encode()).hexdigest()
        self.parent = PageClienteIds()
        super().__init__(aio_id, root='ComponentFiltroClienteIAO')        


class FormComponentBaseClienteIds:
    input_razao_social: str
    input_fantasia: str
    input_email: str
    input_logradouro: str
    input_bairro: str
    btn_trigger_submit: str
    message: str
        
        
class FormComponentADDClienteIds(FormComponentBaseClienteIds, BaseIds):
    
    def __init__(self) -> None:
        aio_id = md5(f'{__name__}-{str(FormComponentADDClienteIds.__name__)}'.encode()).hexdigest()
        self.parent = PageClienteIds()
        super().__init__(aio_id, root=f'ComponentFormADDClienteIAO')
        
      
class FormComponentEDITClienteIds(FormComponentBaseClienteIds, BaseIds):

    def __init__(self) -> None:
        aio_id = md5(f'{__name__}-{str(FormComponentEDITClienteIds.__name__)}'.encode()).hexdigest()
        self.parent = PageClienteIds()
        
        super().__init__(aio_id, root=f'ComponentFormEDITClienteIAO')  