from dash import html
from pyapp.utils.styled_components_util import StyleComponentUtil
from dash.development.base_component import Component


class LayoutPage:
        
    
    def __repr__(self) -> str:
        return 'LAYOUT_PAGE_LOGIN'
    
    def load_data(self) -> None:

        style = StyleComponentUtil()
        style.add_file_scss(name='style.scss', folder_file=__file__, is_base64=True)
        self.Styles = style.link_css
    

    def layout(self, children: Component):
        self.load_data()
        
        return html.Div([self.Styles, html.Section(
            html.Div(
                [
                    html.H1('Auth'),
                    children
                ],     
                className='form-container')
        )])