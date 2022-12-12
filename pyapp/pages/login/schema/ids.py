from pyapp.core.pages.base import BaseIds
from hashlib import md5


class PageLoginIds(BaseIds):
    
    page_url_refresh: str
    message: str
    page_btn_login: str
    page_loading_login: str
    input_username: str
    input_password: str

    def __init__(self) -> None:
        aio_id = md5(f'{__name__}-{str(PageLoginIds)}'.encode()).hexdigest()
        super().__init__(aio_id, root='PageLoginAIO')