from odoo import Odoo
import json
import time
import csv
from variables import *

#Carga de Usuarios
users = open("res.users_load_20191209.json","r")
users_dict = json.loads(users.read())


def transform_extract(records):
    equiv_company_ids = [(3,2),(4,1),(1,3)]
    conn2 = Odoo(url=destination_host,session=destination_session)
    records_final = []
    for record in records:
        if record["user_ids"]:
            if record["user_id"]:
                if users_dict.get(str(record["user_id"]),False):
                    record["user_id"] = users_dict[str(record["user_id"])]["id"]

            if record["create_uid"]:
                if users_dict.get(str(record["create_uid"]),False):
                    record["create_uid"] = users_dict[str(record["create_uid"])]["id"]

            if record.get("company_id"):
                record["company_id"] = [eq[1] for eq in equiv_company_ids
                                                if record.get("company_id") == eq[0]][0]
                                                
            if len(record["user_ids"][0][2]) == 1:
                old_user_id = record["user_ids"][0][2][0]
                new_user_id = users_dict[str(old_user_id)]["id"]
                rec = conn2.call_kw("res.users","search_read",kwargs={"fields":["id","partner_id"],
                                                                "domain":[["id","=",int(new_user_id)]] })
                del record["user_ids"]
                record["write"] = True
                record["new_id"] = rec[0]["partner_id"][0]
                #record.update({"company_id":})
                
            records_final.append(record)

    return records_final


#Descargar datos en Json
conn1 = Odoo(origin_db,origin_user,origin_pass,origin_host)
conn1.authenticate()
fields = ["id","type","name","vat","company_type","city","rfc","x_descuento","trust",
            "street2","street","mobile","email","zip","customer","active","user_id","company_id","over_credit",
            "supplier","employee","parent_id","function","phone","ref","create_uid","credit_limit","zip",
            "uso_cfdi","residencia_fiscal","registro_tributario","x_metodo_pago","x_forma_pago","comment","user_ids"]

file_name = conn1.download_json("res.partner",fields,order="parent_id DESC",
                                                    limit=0,
                                                    transform=transform_extract,
                                                    domain=['|','&',["active","=",0],["active","=",1],["id","not in",[4,5,6]]])

conn2 = Odoo(url=destination_host,session=destination_session)
#conn2.authenticate()
conn2.load_json("res.partner",file_name,dup=True,field_name=True,field_company=True,field_active=True)