from odoo import Odoo
import json
from variables import *

#Carga de invoices
invoices = open("account.invoice_load_20191210.json","r")
invoices_dict = json.loads(invoices.read())
#Carga de invoices
products = open("product.product_load_20191209.json","r")
products_dict = json.loads(products.read())
#Carga de Cuentas
cuentas = open("account.account_load_20191210.json","r")
cuentas_dict = json.loads(cuentas.read())
#Carga de Impuestos
impuestos = open("account.tax_load_20191210.json","r")
impuestos_dict = json.loads(impuestos.read())

def transform(records):
	for record in records:
		record["invoice_id"] = int(invoices_dict[str(record["invoice_id"])]["id"])
		record["product_id"] = int(products_dict[str(record["product_id"])]["id"])
		record["account_id"] = int(cuentas_dict[str(record["account_id"])]["id"])
		record["discount"] = round(record["discount"],2)
		invoice_line_tax_ids = record.get("invoice_line_tax_ids",False)
		if invoice_line_tax_ids:
			record["invoice_line_tax_ids"] = [(6,0,[int(impuestos_dict[str(tax_id)]["id"]) for tax_id in invoice_line_tax_ids[0][2]])]

	return records

#Descargar datos en Json
conn1 = Odoo(origin_db,origin_user,origin_pass,origin_host)

conn1.authenticate()
fields = ["id","name","origin","invoice_id","account_id","quantity","uom_id","discount","price_unit",
        "invoice_line_tax_ids","sequence","product_id","currency_id"]
		
file_name = conn1.download_json("account.invoice.line",fields,
													domain=[["invoice_id","!=",False]],
													transform=transform,
													order="id ASC",limit=0)


conn2 = Odoo(url=destination_host,session=destination_session)


#Eliminar existentes
recs = conn2.call_kw("account.invoice.line","search_read",kwargs={"fields":["id"]})
rec_ids = [rec["id"] for rec in recs]
conn2.call_kw("account.invoice.line","unlink",args=[rec_ids])
#Cargar nuevos
conn2.load_json("account.invoice.line",file_name,threads=35)
