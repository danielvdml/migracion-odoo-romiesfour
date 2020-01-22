from odoo import Odoo
import json
import time
import csv
from variables import *

product_templates = open("product.template_load_20200121.json","r")
product_templates_dict = json.loads(product_templates.read())

uoms = open("product.uom_load_20200121.json","r")
uoms_dict = json.loads(uoms.read())

def transform(record,records):
    record["product_tmpl_id"] = product_templates_dict[str(record["product_tmpl_id"])]["id"]
    record["product_uom_id"] = uoms_dict[str(record["product_uom_id"])]["id"]
    return record


#Descargar datos en Json
conn1 = Odoo(origin_db,origin_user,origin_pass,origin_host)
conn1.authenticate()
fields = ["id","name","product_qty","product_tmpl_id","product_uom_id"]
                    
file_name = conn1.download_json("mrp.bom",fields,
                                            limit=0,
                                            domain=['|',["active","=",0],["active","=",1]])


conn2 = Odoo(destination_db,destination_user,destination_pass,destination_host)
conn2.authenticate()
#Eliminar Productos
#recs = conn2.call_kw("product.product","search_read",kwargs={"fields":["id"]})
#conn2.call_kw("product.product","unlink",args=[[rec["id"] for rec in recs]])
#Cargar Nuevos
conn2.load_json("mrp.bom",file_name,transform=transform,threads=10)