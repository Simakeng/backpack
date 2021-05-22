import sqlite3
import os
from typing import Container, Dict, List
import uuid
from Storage import *
import Storage


def patch_str(x):
    if(type(x) == str):
        return x.replace("'", "''")
    else:
        return x


def sqlite_make_tuple(*args):
    return tuple(map(patch_str, args))


def FindID(db: Any, uuid: str, table: str):
    result = db.execute(
        '''SELECT ID FROM %s WHERE UUID = '%s';''' % sqlite_make_tuple(table, uuid))

    for row in result:
        return row[0]

    raise Exception()


def CreateID(db: Any, uuid: str, table: str):

    db.execute('''INSERT INTO %s(UUID)
        VALUES('%s');''' % sqlite_make_tuple(table, uuid))

    db.commit()

    return FindID(db, uuid, table)


class Database(object):

    def __init__(self, path: str) -> None:
        super().__init__()

        require_init = False
        if not os.path.exists(path):
            require_init = True

        db = sqlite3.connect(path)

        if(require_init):
            # 创建容器表
            db.execute('''CREATE TABLE containers(
                ID          INTEGER     PRIMARY KEY   AUTOINCREMENT ,
                UUID        CHAR(32)    UNIQUE              NOT NULL,
                NAME        TEXT                                    ,
                DATA        TEXT                                    
            );''')

            # 创建单元格表
            db.execute('''CREATE TABLE cells(
                ID          INTEGER     PRIMARY KEY   AUTOINCREMENT ,
                PARENT_ID   INTEGER                                 ,
                UUID        CHAR(32)    UNIQUE              NOT NULL,
                NAME        TEXT                                    ,
                DATA        TEXT                                    
                );''')

            # 创建物品表
            db.execute('''CREATE TABLE items(
                ID          INTEGER     PRIMARY KEY   AUTOINCREMENT ,
                PARENT_ID   INTEGER                                 ,
                UUID        CHAR(32)    UNIQUE              NOT NULL,
                NAME        TEXT                                    ,
                QTY         INTEGER                                 
                );''')

            # 创建属性表
            db.execute('''CREATE TABLE attrs(
                ID          INTEGER     PRIMARY KEY   AUTOINCREMENT ,
                UUID        CHAR(32)    UNIQUE              NOT NULL,
                NAME        TEXT                                    
                );''')

            db.commit()

        self.db = db

    def CreateContainerID(self, uuid: str):
        '''创建一个新的容器ID 分配给实例化的容器对象以进行后续操作'''
        return CreateID(self.db, uuid, "containers")

    def CreateCellID(self, uuid: str):
        '''创建一个新的储存单元ID 分配给实例化的 Cell 对象以进行后续操作'''
        return CreateID(self.db, uuid, "cells")

    def CreateItemID(self, uuid: str):
        '''创建一个新的物品ID 分配给实例化的 Item 对象以进行后续操作'''
        return CreateID(self.db, uuid, "items")

    def CreateAttrClass(self, uuid: str, name: str):
        '''创建一个新的属性类别 分配给实例化的 Item 对象以进行后续操作'''
        if(self.IsAttrClassExists(name)):
            raise Exception("attr class exzists")

        attr_id = CreateID(self.db, uuid, "attrs")

        self.db.execute('''UPDATE attrs SET NAME = '%s' WHERE ID = %d;''' %
                        sqlite_make_tuple(name, attr_id))

        self.db.execute('''CREATE TABLE attr_%s(
            ITEM_ID     INTEGER     PRIMARY KEY  UNIQUE,
            VALUE       TEXT 
        );''' % name)

        return attr_id

    def LoadContainers(self) -> List:
        containers = {}
        cursor = self.db.execute(
            '''SELECT ID,UUID,NAME,DATA FROM containers;''')

        for storage_id, uid, name, data in cursor:
            cont = Matrix()
            cont.storage_id = storage_id
            cont.uuid = uid
            cont.name = name
            cont.flaten_data = data
            cont.cells = [[None for _ in range(
                cont.storage_y)] for _ in range(cont.storage_x)]
            containers[storage_id] = cont

        cursor = self.db.execute(
            '''SELECT ID,PARENT_ID,UUID,NAME,DATA FROM cells;''')
        cells = {}
        for storage_id, parent_id, uid, name, data in cursor:
            cell = Cell(containers[parent_id])
            cell.name = name
            cell.uuid = uid
            cell.storage_id = storage_id
            cell.flaten_data = data

            index = cell.get_index()

            containers[parent_id].cells[index[0]][index[1]] = cell
            cells[storage_id] = cell

        items = {}
        cursor = self.db.execute(
            '''SELECT ID,PARENT_ID,UUID,NAME FROM items;''')
        for storage_id, parent_id, uid, name in cursor:
            item = Item()
            item.storage_id = storage_id
            item.parent = cells[storage_id]
            item.uuid = uid
            cells[parent_id].add_item(item)
            items[storage_id] = item

        cursor = self.db.execute(
            '''SELECT ID,UUID,NAME FROM attrs;''')
        
        for storage_id,uid,name in cursor:
            sql = '''SELECT ITEM_ID,VALUE FROM attr_%s''' % name
            attr_values = self.db.execute(sql)
            for item_id,value in attr_values:
                items[item_id][name] = value

        return list(containers.values())
        
    # def GetAttrClassInfo(self, name: str) -> Any:
    #     result = self.db.execute(
    #         '''SELECT ID,UUID,NAME FROM attrs WHERE NAME='%s';''' % patch_str(name))
    #     for row in result:
    #         return {
    #             "id": row[0],
    #             "uuid": row[1],
    #             "name": row[2],
    #         }
    #     return None

    # def GetAttrClassUUID(self, name: str) -> Any:
    #     result = self.db.execute(
    #         '''SELECT ID FROM attrs WHERE NAME='%s';''' % patch_str(name))
    #     for row in result:
    #         return row[0]
    #     return None

    def GetAttrClassID(self, name: str) -> Any:
        result = self.db.execute(
            '''SELECT ID FROM attrs WHERE NAME='%s';''' % patch_str(name))
        for row in result:
            return row[0]
        return None

    def IsAttrClassExists(self, name: str) -> bool:

        id = self.GetAttrClassID(name)
        if(id != None):
            return True
        else:
            return False

    def SetContainerInfo(self, cont: ContainerInterface):
        self.db.execute('''\
        INSERT OR REPLACE INTO containers
        (ID,UUID,NAME,DATA)
        VALUES(%d,'%s','%s','%s')
        ''' % sqlite_make_tuple(cont.storage_id, cont.uuid, cont.name, cont.flaten_data))

        self.db.commit()
        pass

    def SetCellInfo(self, cell: Cell):
        parent_id = None
        if(cell.parent != None):
            parent_id = cell.parent.storage_id
        else:
            parent_id = "NULL"

        self.db.execute('''\
        INSERT OR REPLACE INTO cells
        (ID,PARENT_ID,UUID,NAME,DATA)
        VALUES(%d,%s,'%s','%s','%s')
        ''' % sqlite_make_tuple(cell.storage_id, parent_id, cell.uuid, cell.name, cell.flaten_data))

        self.db.commit()

    def UpdateItemInfo(self, item: Item):
        parent_id = None
        if(item.parent != None):
            parent_id = item.parent.storage_id
        else:
            parent_id = "NULL"
        self.db.execute('''\
        INSERT OR REPLACE INTO items 
        (ID,PARENT_ID,UUID,NAME,QTY) 
        VALUES( %d,%s,'%s','%s',%d );
        ''' % sqlite_make_tuple(item.storage_id, str(parent_id),
                                item.uuid, item.name, item.quantity))

        self.db.commit()

    def SetItemAttr(self, item_storage_id, attr_name, attr_value) -> None:
        self.db.execute(
            '''INSERT OR REPLACE INTO attr_%s 
        (ITEM_ID,VALUE) 
        VALUES(%d,'%s')
        ''' % sqlite_make_tuple(attr_name, item_storage_id, attr_value))

        self.db.commit()

        return

    def RemoveItemAttr(self, item_storage_id, attr_name) -> None:
        self.db.execute(
            '''DELETE FROM attr_%s WHERE ITEM_ID = %d;''' % sqlite_make_tuple(attr_name, item_storage_id))
        self.db.commit()
        return

    def GetItemAttrs(self, item: Item) -> Dict:
        result = self.db.execute('''SELECT ID,NAME FROM attrs;''')
        list_attrs = [row for row in result]
        item_attrs = {}
        for _, attr_name in list_attrs:
            result = self.db.execute('''SELECT VALUE FROM attr_%s WHERE ITEM_ID = %d;''' %
                                     sqlite_make_tuple(attr_name, item.storage_id)).fetchall()
            if(len(result) == 0):
                continue
            elif(len(result) == 1):
                item_attrs[attr_name] = result[0][0]
        return item_attrs
