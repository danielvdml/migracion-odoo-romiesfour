from odoo import Odoo
import json
from variables import *

def transform(records):
    equiv_company_ids = [(3,2),(4,1),(1,3)]
    for record in records:
        if record.get("company_id"):
            record["company_id"] = [eq[1] for eq in equiv_company_ids
                                            if record.get("company_id") == eq[0]][0]
    return records


#Descargar datos en Json
conn1 = Odoo(origin_db,origin_user,origin_pass,origin_host)
conn1.authenticate()
fields = ["id","code","name","user_type_id","tag_ids","company_id","deprecated","tax_ids"]
file_name = conn1.download_json("account.account",fields,transform=transform,limit=0)


conn2 = Odoo(url=destination_host,session=destination_session)
conn2.load_json("account.account",file_name,dup=True,field_name=True,field_company=True)
