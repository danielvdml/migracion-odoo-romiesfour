from odoo import Odoo
import json
from variables import *

#Carga de Sale Orders
sale_order = open("sale.order_load_20191210.json","r")
sale_order_dict = json.loads(sale_order.read())
#Carga de Products
products = open("product.product_load_20191209.json","r")
products_dict = json.loads(products.read())
#carga de Impuestos
impuestos = open("account.tax_load_20191210.json","r")
impuestos_dict = json.loads(impuestos.read())

def transform(records):
	for record in records:
		record["order_id"] = sale_order_dict[str(record["order_id"])]["id"]
		record["product_id"] = int(products_dict[str(record["product_id"])]["id"])

		tax_id = record.get("tax_id",False)
		if tax_id:
			record["tax_id"] = [(6,0,[int(impuestos_dict[str(tax_id)]["id"]) for tax_id in tax_id[0][2]])]

		record["discount"] = round(record["discount"],2)
	return records

#Descargar datos en Jsons
conn1 = Odoo(origin_db,origin_user,origin_pass,origin_host)
conn1.authenticate()
fields = ["id","name","product_id","product_uom_qty","product_uom",
			"price_unit","tax_id","purchase_price","order_id","discount","customer_lead"]
file_name = conn1.download_json("sale.order.line",fields,
													domain=[["order_id","!=",False],["order_id.partner_id","not in",[1,2,3,4,5,6]]],
													transform=transform,
													order="id ASC",limit=0)

conn2 = Odoo(url=destination_host,session=destination_session)
#conn2.authenticate()
#Eliminar existentes
recs = conn2.call_kw("sale.order.line","search_read",kwargs={"fields":["id"]})
rec_ids = [rec["id"] for rec in recs]
conn2.call_kw("sale.order.line","unlink",args=[rec_ids])
#Cargar nuevos
conn2.load_json("sale.order.line",file_name,threads=30)
