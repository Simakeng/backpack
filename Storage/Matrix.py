from Storage.ContainerInterface import Cell, ContainerInterface


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
