from odoo import Odoo
import json
import time
import csv
from variables import *

boms = open("mrp.bom_load_20200121.json","r")
boms_dict = json.loads(boms.read())

products = open("product.product_load_20200121.json","r")
products_dict = json.loads(products.read())

uoms = open("product.uom_load_20200121.json","r")
uoms_dict = json.loads(uoms.read())

def transform(record,records):
    record["bom_id"] = boms_dict[str(record["bom_id"])]["id"]
    record["product_id"] = products_dict[str(record["product_id"])]["id"]
    record["product_uom_id"] = uoms_dict[str(record["product_uom_id"])]["id"]
    return record


#Descargar datos en Json
conn1 = Odoo(origin_db,origin_user,origin_pass,origin_host)
conn1.authenticate()
fields = ["id","product_qty","product_id","product_uom_id","bom_id"]
                    
file_name = conn1.download_json("mrp.bom.line",fields,
                                            limit=0,
                                            domain=[])


conn2 = Odoo(destination_db,destination_user,destination_pass,destination_host)
conn2.authenticate()
#Eliminar Productos
#recs = conn2.call_kw("product.product","search_read",kwargs={"fields":["id"]})
#conn2.call_kw("product.product","unlink",args=[[rec["id"] for rec in recs]])
#Cargar Nuevos
conn2.load_json("mrp.bom.line",file_name,transform=transform,threads=20)