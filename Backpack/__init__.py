from Storage import *
from Database import *
import uuid


class Backpack(object):
    def __init__(self, data_path) -> None:
        super().__init__()
        self.db = Database(data_path)
        self.containers = []

    def CreateMatrixContainer(self, name, x, y, cell_size):
        """Create a matrix typed container"""
        m = Matrix()
        m.storage_x = x
        m.storage_y = y
        m.name = name
        m.uuid = uuid.uuid4().hex.upper()
        cid = self.db.CreateContainerID(m.uuid)
        m.storage_id = cid
        for i in range(x):
            row = []
            for j in range(y):
                cell = Cell(m)
                cell.name = f"{name}::cell_{i}_{j}"
                cell.capacity = 1
                cell.uuid = uuid.uuid4().hex.upper()
                cell.cell_index = (i, j)
                cell.storage_id = self.db.CreateCellID(cell.uuid)
                row.append(cell)
            m.cells.append(row)
        return m

    def CreateItem(self):
        item = Item()
        item.uuid = uuid.uuid4().hex.upper()
        item.storage_id = self.db.CreateItemID(item.uuid)
        return item

    def UpdateContainer(self, cont: ContainerInterface):
        self.db.SetContainerInfo(cont)
        for cell in cont:
            self.UpdateCell(cell)
        pass

    def UpdateCell(self, cell: Cell):
        self.db.SetCellInfo(cell)
        for item in cell:
            self.db.UpdateItemInfo(item)

    def UpdateItemAttrs(self, item: Item):
        stored_attrs = self.db.GetItemAttrs(item)
        attr_need_remove = []
        attr_need_update = []

        for k, v in stored_attrs.items():
            if(not k in item.attrs.keys()):
                attr_need_remove.append(k)
            else:
                if(v != str(item.attrs[k])):
                    attr_need_update.append(k)

        for k, v in item.attrs.items():
            if(not k in stored_attrs.keys()):
                attr_need_update.append(k)

        for k in attr_need_remove:
            self.db.RemoveItemAttr(item.storage_id, k)
            pass

        for k in attr_need_update:
            v = item.attrs[k]
            if(not self.db.IsAttrClassExists(k)):
                self.db.CreateAttrClass(uuid.uuid4().hex.upper(), k)
            self.db.SetItemAttr(item.storage_id, k, v)
