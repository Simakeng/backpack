from typing import Any


class Item(object):
    def __init__(self) -> None:
        super().__init__()
        self.attrs = {}
        self.uuid = None
        self.storage_id = None
        self.parent = None

    @property
    def name(self) -> str:
        if("name" in self.attrs.keys()):
            return self.attrs["name"]
        else:
            return "Unnamed Item"

    @property
    def quantity(self) -> int:
        if("quantity" in self.attrs.keys()):
            return self.attrs["quantity"]
        else:
            return 0

    def get_attr(self, name: str) -> Any:
        return self.attrs[name]

    def set_attr(self, name: str, value: Any) -> None:
        self.attrs[name] = value

    def __getitem__(self, name: str) -> Any:
        return self.get_attr(name)

    def __setitem__(self, name: str, value: Any) -> None:
        self.set_attr(name, value)

    def __delitem__(self, name: str) -> Any:
        del self.attrs[name]


class Cell:
    def __init__(self, parent) -> None:
        self.uuid = "id not assigned"
        self.cell_index = None
        self.storage_id = None
        self.content = set()
        self.capacity = 0
        self.name = ""
        self.parent = parent
        pass

    def get_name(self) -> str:
        return self.name

    def get_uuid(self) -> str:
        return self.uuid

    def get_index(self):
        return self.cell_index

    def get_capacity(self) -> Any:
        return self.capacity

    def get_content(self):
        return self.content

    def add_item(self, item: Item):
        if(item in self.content):
            raise Exception("item '%s' aleady in cell '%s'" %
                            (item.name, self.name))
        self.content.add(item)
        item.parent = self
        pass
    
    def __iter__(self):
        return self.content.__iter__()

    def remove_item(self, item: Item):
        pass

    @property
    def flaten_data(self) -> str:
        return ""


class ContainerInterface(object):
    def __init__(self) -> None:
        self.uuid = "id not assigned"
        self.name = ""
        self.storage_id = None
        pass

    def get_uuid(self):
        return self.uuid

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

    def get_cell(self, cell_index) -> Cell:
        c = Cell()
        c.cell_index = cell_index
        return c

    def cell(self, cell_index) -> Cell:
        return self.get_cell(cell_index)

    def __getitem__(self, cell_id) -> Cell:
        return self.get_cell(cell_id)

    @property
    def flaten_data(self) -> str:
        return ""
