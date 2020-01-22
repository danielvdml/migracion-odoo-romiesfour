from odoo import Odoo
import json
from variables import *

#Carga de Clientes
partners = open("res.partner_load_20191210.json","r")
partners_dict = json.loads(partners.read())
#Carga de Usuarios
users = open("res.users_load_20191209.json","r")
users_dict = json.loads(users.read())
#Carga de Almacenes
almacenes = open("stock.warehouse_load_20191210.json","r")
almacenes_dict = json.loads(almacenes.read())

def transform_extract(records):
    equiv_company_ids = [(3,2),(4,1),(1,3)]
    for record in records:
        record["partner_id"] = partners_dict[str(record["partner_id"])]["id"]
        if record.get("company_id"):
            record["company_id"] = [eq[1] for eq in equiv_company_ids
                                            if record.get("company_id") == eq[0]][0]
        if record["user_id"]:
            if users_dict.get(str(record["user_id"]),False):
                record["user_id"] = users_dict[str(record["user_id"])]["id"]

        if record["warehouse_id"]:
            if almacenes_dict.get(str(record["warehouse_id"]),False):
                record["warehouse_id"] = almacenes_dict[str(record["warehouse_id"])]["id"]

    return records
    
#Descargar datos en Json
conn1 = Odoo(origin_db,origin_user,origin_pass,origin_host)
conn1.authenticate()
fields = ["id","name","partner_id","confirmation_date","tipo_documento","state","date_order","company_id",
        "validity_date","user_id","uso_cfdi","forma_pago","methodo_pago","discount_rate",
        "invoice_status","origin","warehouse_id","payment_term_id"]

file_name = conn1.download_json("sale.order",fields,transform=transform_extract,
                                                        order="id ASC",
                                                        limit=0,domain=[["partner_id","not in",[1,2,3,4,5,6]]])

#Conexión a Nueva Instancia
conn2 = Odoo(url=destination_host,session=destination_session)
#conn2.authenticate()
#Eliminar existentes
recs = conn2.call_kw("sale.order","search_read",kwargs={"fields":["id"]})
rec_ids = [int(rec["id"]) for rec in recs]
print(rec_ids)
if conn2.call_kw("sale.order","write",args=[rec_ids,{"state":"draft"}]):
    print("Actualización a borrador")
else:
    print("No se puedo actualziar")


if conn2.call_kw("sale.order","unlink",args=[rec_ids]):
    print("eliminacion de Ventas")

conn2.load_json("sale.order",file_name,threads=35)