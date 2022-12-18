from abc import ABC, abstractmethod, abstractproperty
from typing import List
from dash import strip_relative_path, dependencies
from pyapp.components.bread_crumb import ComponentBreadCrumbs
    
class BasePageABC(ABC):
    
    @abstractproperty
    def template_path(self) -> List[str]:
        raise NotImplementedError
    
    @abstractmethod
    def events(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def layout(self, *args, **kwargs) -> dependencies.Component:
        raise NotImplementedError
        
    @abstractproperty
    def title(self) -> str:
        raise NotImplementedError
    
    
    # @abstractproperty
    # def path(self) -> str:
    #     raise NotImplementedError
           
    
    # @abstractproperty.setter
    # def path(self, current_url) -> None:
    #     raise NotImplementedError
    
    
    

class BaseIds:

        def __init__(self, aio_id, root) -> None:
            self.aio_id = aio_id
            self.root = root
            self.__map__()

        def __map__(self):
            for _property in self.__annotations__.keys():
                setattr(self, _property,
                        f'{self.root}-{_property}-{self.aio_id}')

class BasePage(BasePageABC):

    @property
    def path(self):
        return self._path
           
    
    @path.setter
    def path(self, current_url):
        self._path = current_url
        
        
    @property
    def breadcrumb(self):
        return ComponentBreadCrumbs().layout(self.path)