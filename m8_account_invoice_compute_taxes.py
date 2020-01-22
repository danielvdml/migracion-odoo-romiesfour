from odoo import Odoo
import json
from variables import *

conn2 = Odoo(url=destination_host,session=destination_session)
#conn2 = Odoo(origin_db,origin_user,origin_pass,origin_host)
#conn2.authenticate()

recs = conn2.call_kw("account.invoice","search_read",kwargs={"fields":["id"]})
rec_ids = [rec["id"] for rec in recs]
print(rec_ids)
#print(conn2.call_kw("account.invoice","write",args=[rec,{"move_name":"","name":"","state":"draft"}]))
salto = 30
for rec in [rec_ids[x:x+salto] for x in range(0,len(rec_ids),salto)]:
    print(rec)
    conn2.call_kw("account.invoice","compute_taxes",args=[rec])