from odoo import Odoo
import json
import time
import csv
from variables import *


def transform(record,records):
    record["factor_inv"] = record["factor"]
    return record

#Descargar datos en Json
conn1 = Odoo(origin_db,origin_user,origin_pass,origin_host)
conn1.authenticate()
fields = ["id","name","category_id","uom_type","rounding","factor"]
                    
file_name = conn1.download_json("product.uom",fields,
                                            limit=0,
                                            domain=['|',["active","=",0],["active","=",1]])


conn2 = Odoo(destination_db,destination_user,destination_pass,destination_host)
conn2.authenticate()
#Eliminar Productos
#recs = conn2.call_kw("product.product","search_read",kwargs={"fields":["id"]})
#conn2.call_kw("product.product","unlink",args=[[rec["id"] for rec in recs]])
#Cargar Nuevos
conn2.load_json("product.uom",file_name,transform=transform,dup=True,field_name=True)