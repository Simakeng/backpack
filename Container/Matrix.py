from Container.ContainerInterface import ContainerInterface



class Matrix(ContainerInterface):

    def __init__(self, x, y) -> None:
        super().__init__()
        self.storage_x = x
        self.storage_y = y

    def get_desc(self):
        return '''[Matrix Storage Class]
multiple Cell storage arranged as X,Y dimension'''

    def get_capacity(self):
        return (self.storage_x, self.storage_y)
