from Storage.ContainerInterface import Cell, ContainerInterface
import json


class Matrix(ContainerInterface):

    def __init__(self) -> None:
        super().__init__()
        self.storage_x = 0
        self.storage_y = 0
        self.cells = []

    def get_desc(self):
        return '''[Matrix Storage Class]
multiple Cell storage arranged as X,Y dimension'''

    def get_capacity(self):
        return (self.storage_x, self.storage_y)

    def get_cell(self, cell_index) -> Cell:
        if(type(cell_index) == tuple):
            if(len(cell_index) != 2):
                raise Exception("Cell Index is not a acceptable type!")
            if(cell_index[0] >= self.storage_x):
                raise Exception("index %s is not in this Matrix '%s' %s" %
                                (cell_index, self.name, str((self.storage_x, self.storage_y))))
            if(cell_index[1] >= self.storage_y):
                raise Exception("index %s is not in this Matrix '%s' %s" %
                                (cell_index, self.name, str((self.storage_x, self.storage_y))))

            return self.cells[cell_index[0]][cell_index[1]]
        elif(type(cell_index) == int):
            i = cell_index // self.storage_y
            j = cell_index % self.storage_y
            if(i >= self.storage_x):
                raise StopIteration()
            r = self.cells[i][j]
            return r

    def set_cell(self, cell_index, value) -> Cell:
        if(type(cell_index) == tuple):
            if(len(cell_index) != 2):
                raise Exception("Cell Index is not a acceptable type!")
            if(cell_index[0] >= self.storage_x):
                raise Exception("index %s is not in this Matrix '%s' %s" %
                                (cell_index, self.name, str((self.storage_x, self.storage_y))))
            if(cell_index[1] >= self.storage_y):
                raise Exception("index %s is not in this Matrix '%s' %s" %
                                (cell_index, self.name, str((self.storage_x, self.storage_y))))
        elif(type(cell_index) == int):
            i = cell_index // self.storage_y
            j = cell_index % self.storage_y
            if(i >= self.storage_x):
                raise StopIteration()
            self.cells[i][j] = value
            r = self.cells[i][j]
            return r

    @property
    def flaten_data(self) -> str:
        return json.dumps({
            "type": type(self).__name__,
            "storage_x": self.storage_x,
            "storage_y": self.storage_y,
        })

    @flaten_data.setter
    def flaten_data(self, value):
        data = json.loads(value)
        self.storage_x = data["storage_x"]
        self.storage_y = data["storage_y"]
