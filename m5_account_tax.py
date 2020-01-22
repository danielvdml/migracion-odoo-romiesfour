from odoo import Odoo
import json
from variables import *

#Carga de Cuentas
cuentas = open("account.account_load_20191210.json","r")
cuentas_dict = json.loads(cuentas.read())


def transform(records):
    equiv_company_ids = [(3,2),(4,1),(1,3)]
    for record in records:
        if record.get("account_id",False):
            record["account_id"] = int(cuentas_dict[str(record["account_id"])]["id"])
        if record.get("cash_basis_base_account_id",False):
            record["cash_basis_base_account_id"] = int(cuentas_dict[str(record["cash_basis_base_account_id"])]["id"])
        if record.get("cash_basis_account_id",False):
            record["cash_basis_account_id"] = int(cuentas_dict[str(record["cash_basis_account_id"])]["id"])
        if record.get("company_id"):
            record["company_id"] = [eq[1] for eq in equiv_company_ids
                                            if record.get("company_id") == eq[0]][0]
    return records


#Descargar datos en Json
conn1 = Odoo(origin_db,origin_user,origin_pass,origin_host)
conn1.authenticate()
fields = ["id","company_id","name","type_tax_use","account_type","amount","description","account_id",
            "tax_exigibility","cash_basis_account_id","cash_basis_base_account_id","tag_ids",
            "tax_group_id","price_include","incluse_base_amount","impuesta","tipo_factor","active"]

file_name = conn1.download_json("account.tax",fields,transform=transform,limit=0,
                                                domain=['|',["active","=",0],["active","=",1]])


conn2 = Odoo(url=destination_host,session=destination_session)
conn2.load_json("account.tax",file_name,dup=True,field_name=True,field_active=True,field_company=True)
