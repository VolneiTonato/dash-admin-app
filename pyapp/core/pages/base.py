from abc import ABC, abstractmethod
from typing import List

  
    
class BasePageABC(ABC):
    
    @abstractmethod
    def urls_paths(self) -> List[str]:
        raise NotImplementedError
    

class BaseIds:

        def __init__(self, aio_id, root) -> None:
            self.aio_id = aio_id
            self.root = root
            self.__map__()

        def __map__(self):
            for _property in self.__annotations__.keys():
                setattr(self, _property,
                        f'{self.root}-{_property}-{self.aio_id}')

class BasePage:

    @property
    def path(self):
        return self._path
           
    
    @path.setter
    def path(self, current_url):
        self._path = current_url