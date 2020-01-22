from odoo import Odoo
conn = Odoo("santaclara_db_1","admin","admin","localhost:8827",False)
conn.authenticate()

l  =conn.call_kw("product.product","search_read",
                    kwargs={'fields':['name','product_tmpl_id',"list_price"],'limit':10,'domain':[['name','ilike','3XXX MARACUYA 1.8LT']]})

print(l)
l  =conn.call_kw("product.product","read",[[5494],["name",'display_name']],kwargs={"context":{"bin_size":True,"params":{"action":119}}})
                          
print(l)
conn.call_kw("product.template","write",[[5495],{"name":"3XXX MARACUYA 1.8LT *XYZ123*****","list_price":2003.33}])
#l  =conn.call_kw("product.template","read",args=[[5495],['name']])
#print(l)
#DOWNLOAD PARTNERS
"""
fields = ["id","type","name","catalog_06_id","vat","company_type","estado_contribuyente",
            "registration_name","street","mobile","email","zip","customer",
            "supplier","linea_credito","employee","parent_id","function","phone"]
"""
#conn.download_json("res.partner",fields,order="parent_id DESC",limit=0)



#DOWNLOAD LÍNEA DE COMPROBANTES
fields = []
#conn.download_json("account.invoice.line",fields)

#DOWNLOAD COMPROBANTES
"""
fields = ["id","number","move_name","date_order","partner_id","journal_id","tipo_operacion",
            "tiene_guia_remision","numero_guia_remision","user_id","tipo_cambio",
            "currency_id","digest_value","invoice_line_ids","period_id","origin",
            "tipo_operacion"]
"""
#conn.download_json("account.invoice",fields)

X = conn.call_kw("ir.translation","search_read",[],{'domain':[['name','=','product.template,name']]})
for x in X:
    if not (x["source"] != x["value"] and x["source"] == False):
        print((x["source"] or "").ljust(50),x["value"])
    