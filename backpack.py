from Storage.ContainerInterface import Item
from Storage import Item

import Backpack
import os

os.remove("test.db")
pack = Backpack.Backpack("test.db")
item = pack.CreateItem()
item["name"] = "10K 0603 贴片电阻"
item["category"] = "贴片电阻"
item["ic_package"] = "R0603"
item["resistor_value"] = "103"
item["taobao_price"] = 0.01
item["quantity"] = 1000

m = pack.CreateMatrixContainer("test_case", 15, 3, 100)
m[(1, 2)].add_item(item)
pack.UpdateItemAttrs(item)
item["quantity"] = 100
item["sb"] = "test"
del item["taobao_price"]

pack.UpdateContainer(m)

pass
