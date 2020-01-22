from odoo import Odoo
import json
import time
import csv
from variables import *

uoms = open("product.uom_load_20200121.json","r")
uoms_dict = json.loads(uoms.read())
def transform(record,records):
    record["uom_id"] = uoms_dict[str(record["uom_id"])]["id"]
    record["uom_po_id"] = uoms_dict[str(record["uom_po_id"])]["id"]
    return record


#Descargar datos en Json
conn1 = Odoo(origin_db,origin_user,origin_pass,origin_host)
conn1.authenticate()
fields = ["id","name","sale_ok","purchase_ok","type","default_code","lst_price",
            "standard_price","uom_id","uom_po_id","active",
            "description_sale","image"]
                    
file_name = conn1.download_json("product.product",fields,
                                            limit=0,
                                            domain=['|',["active","=",0],["active","=",1]])


conn2 = Odoo(destination_db,destination_user,destination_pass,destination_host)
conn2.authenticate()
#Eliminar Productos
#recs = conn2.call_kw("product.product","search_read",kwargs={"fields":["id"]})
#conn2.call_kw("product.product","unlink",args=[[rec["id"] for rec in recs]])
#Cargar Nuevos
conn2.load_json("product.product",file_name,transform=transform,dup=True,field_name=True,threads=10)