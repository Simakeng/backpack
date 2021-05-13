from typing import Any


class ContainerInterface(object):
    def __init__(self) -> None:
        self.item_id = "id not assigned"
        pass

    def get_id(self):
        return self.item_id

    def get_desc(self) -> str:
        return "Default Container Interface"

    @property
    def desc(self) -> str:
        return self.get_desc()
    
    def get_capacity(self):
        return None

    @property
    def capacity(self):
        return self.get_capacity()
    
    def is_empty(self):
        return False

    @property
    def empty(self):
        return self.is_empty()

    def get_cell(self,cell_id):
        return None

    @property
    def cell(cell_id):
        c = CellInterface()
        c.item_id = cell_id
        return c

    def __getitem__(self,cell_id):
        return self.get_cell(cell_id)

    
class CellInterface:
    def __init__(self) -> None:
        self.item_id = "id not assigned"
        self.content = []
        pass

    def get_id(self) -> str:
        return self.item_id

    def get_volume(self) -> Any:
        return 0
    
    def get_content(self):
        return self.content
    
