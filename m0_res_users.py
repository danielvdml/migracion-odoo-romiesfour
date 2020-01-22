from odoo import Odoo
import json
import time
import csv
import os
from variables import *

def transform_extract(records):
    equiv_company_ids = [(3,2),(4,1),(1,3)]
    for record in records:
        record["customer"] = False
        record["employee"] = True
        record["email"] = record["login"]
        #record["password"] = record["login"]
        if record.get("company_ids"):
            record["company_ids"] = [(6,0,[eq[1] for c in record.get("company_ids")[0][2] 
                                                    for eq in equiv_company_ids 
                                                        if c == eq[0]])]
        if record.get("company_id"):
            record["company_id"] = [eq[1] for eq in equiv_company_ids
                                            if record.get("company_id") == eq[0]][0]
        
    return records


#Descargar datos en Json
conn1 = Odoo(origin_db,origin_user,origin_pass,origin_host)
conn1.authenticate()
fields = ["id","name","login","email",
            "mobile","phone","employee","tz_offset","signature",
            "street","active","customer","employee","share",
            "company_ids","company_id","lang","state"]

file_name = conn1.download_json("res.users",fields,limit=0,
                                                    domain=['|',["active","=",True],["active","=",False]],
                                                    transform=transform_extract)

#conn2 = Odoo(destination_db,destination_user,destination_pass,destination_host)
conn2 = Odoo(url=destination_host,session=destination_session)
#conn2.authenticate()

conn2.load_json("res.users",file_name,dup=True,field_login=True,field_active=True,field_company=True)