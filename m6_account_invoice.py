from odoo import Odoo
import json
from variables import *


#Carga de Clientes
partners = open("res.partner_load_20191210.json","r")
partners_dict = json.loads(partners.read())
#Carga de Diarios-Series
journals = open("account.journal_load_20191210.json","r")
journals_dict = json.loads(journals.read())
#Carga de Usuarios
users = open("res.users_load_20191209.json","r")
users_dict = json.loads(users.read())
#Carga de Cuentas
cuentas = open("account.account_load_20191210.json","r")
cuentas_dict = json.loads(cuentas.read())


def transform_extract(records):
    equiv_company_ids = [(3,2),(4,1),(1,3)]
    for record in records:
        if record.get("company_id",False):
            record["company_id"] = [eq[1] for eq in equiv_company_ids
                                            if record.get("company_id") == eq[0]][0]
        record["partner_id"] = partners_dict[str(record["partner_id"])]["id"]
        record["journal_id"] = journals_dict[str(record["journal_id"])]["id"]
        if record["user_id"]:
            if users_dict.get(str(record["user_id"]),False):
                record["user_id"] = users_dict[str(record["user_id"])]["id"]
        record["name"] = record["move_name"]
        if record.get("account_id",False):
            record["account_id"] = int(cuentas_dict[str(record["account_id"])]["id"])
        record["discount_rate"] = round(record["discount_rate"],2)
        
    return records
    
def transform_load(record,records):
    if record.get("refund_invoice_id",False):
        try:
            record["refund_invoice_id"] = records[record["refund_invoice_id"]]["id"]
        except Exception as e:
            pass
    return record

#Descargar datos en Json
conn1 = Odoo(origin_db,origin_user,origin_pass,origin_host)
conn1.authenticate()
fields = ["number","move_name","partner_id","journal_id","name",
            "user_id","tipo_comprobante","uso_cfdi","forma_pago","methodo_pago",
            "currency_id","origin","folio_fiscal","tipo_relacion",
            "reference","type","uuid_relacionado","fecha_factura",
            "refund_invoice_id","estado_factura","confirmacion",
            "date_due","date_invoice","state","company_id","account_id","discount_rate",
            "uuid_relacionado","confirmacion","discount","monto","precio_unitario",
            "monto_impuesto","decimales","desc","qr_value","invoice_datetime",
            "fecha_factura","rfc_emisor","name_emisor","serie_emisor","tipo_relacion",
            "numero_cetificado","cetificaso_sat","folio_fiscal","fecha_certificacion",
            "cadena_origenal","selo_digital_cdfi","selo_sat","moneda","tipocambio",
            "folio","version","number_folio","amount_to_text","pdf_cdfi_invoice",
            "qrcode_image","regimen_fiscal","xml_invoice_link","estado_factura",
            "factura_cfdi","tipo_comprobante","forma_pago"]

file_name = conn1.download_json("account.invoice",fields,transform=transform_extract,
                                                        order="refund_invoice_id ASC",
                                                        limit=0)

conn2 = Odoo(url=destination_host,session=destination_session)
#conn2.authenticate()

#conn2.call_kw("account.invoice","write",args=[[1455],{"move_name":"","name":"","state":"draft"}])
#conn2.call_kw("account.invoice","unlink",args=[[1455]])
#Eliminar existentes

""""""
recs = conn2.call_kw("account.invoice","search_read",kwargs={"fields":["id"]})
rec_ids = [int(rec["id"]) for rec in recs]
print(rec_ids)


for rec in [rec_ids[x:x+20] for x in range(0,len(rec_ids),20)]:
    print(rec)
    print(conn2.call_kw("account.invoice","write",args=[rec,{"move_name":"","name":"","state":"draft"}]))

for rec in [rec_ids[x:x+20] for x in range(0,len(rec_ids),20)]:
    print(rec)
    print(conn2.call_kw("account.invoice","unlink",args=[rec]))

#conn2.load_json("account.invoice",file_name,dup=True,transform=transform_load,field_name=True,field_company=True)
conn2.load_json("account.invoice",file_name,transform=transform_load,field_company=True)
