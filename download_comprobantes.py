from odoo import Odoo
import json
import time
import xlwt
import csv


"""
def jsontorow(jsonx):
    row = []
    for j in jsonx:
        if type(jsonx[j]) == list and len(jsonx[j]) == 2:
            if type(jsonx[j][0]) == int  and type(jsonx[j][1]) == str:
                row.append(jsonx[j][1])
        else:
            row.append(jsonx[j])
    return row

def download_json_account_invoice(limit=10):
    account_invoices_json = open("account_invoices.json","w")
    fields = ["number","move_name","date_order","partner_id","journal_id","tipo_operacion",
                "tiene_guia_remision","numero_guia_remision","user_id","tipo_cambio",
                "currency_id","digest_value","invoice_line_ids","period_id","origin",
                "tipo_operacion"]
    kwargs = {"fields":fields}
    if limit>0:
        kwargs.update({"limit":limit})
    invoices = conn.call_kw("account.invoice","search_read",[[]],kwargs)
    rows = []
    for inv in invoices:
        rows.append(jsontorow(inv))
        
    return rows


def download_xlsx_partner(name_file,limit=10):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('res.partner')

    fields = ["name","catalog_06_id","vat","company_type","estado_contribuyente",
                "registration_name","street","mobile","email","zip","country_id",
                "state_id","province_id","district_id","customer","supplier","linea_credito"]
    kwargs = {"fields":fields}
    if limit>0:
        kwargs.update({"limit":limit})
    partners = conn.call_kw("res.partner","search_read",[[]],kwargs)

    for i,field in enumerate(fields):
        ws.write(0,i,field)

    for r,partner in enumerate(partners):
        print(partner)
        name = partner["name"]
        if partner["catalog_06_id"]:
            print(partner["catalog_06_id"][0])
            catalog_06_id = str(partner["catalog_06_id"][0])
        else:
            catalog_06_id = "-"
        vat = partner["vat"] if partner["vat"] else ""
        company_type = partner["company_type"] if partner["company_type"] else ""
        estado_contribuyente = partner["estado_contribuyente"] if partner["estado_contribuyente"] else ""
        registration_name = partner["registration_name"] if partner["registration_name"] else ""
        street = partner["street"] if partner["street"] else ""
        mobile = partner["mobile"] if partner["mobile"] else ""
        email = partner["email"] if partner["email"] else ""
        ubigeo = partner["zip"] if partner["zip"] else ""
        country_id = str(partner["country_id"][0] if partner["country_id"] else "")
        state_id = str(partner["state_id"][0] if partner["state_id"] else "")
        province_id = str(partner["province_id"][0] if partner["province_id"] else "")
        district_id = str(partner["district_id"][0] if partner["district_id"] else "")
        customer = str(partner["customer"])
        supplier = str(partner["supplier"])
        linea_credito = str(partner["linea_credito"])
        columns = [name,catalog_06_id,vat,company_type,estado_contribuyente,
                    registration_name,street,mobile,email,ubigeo,country_id,
                    state_id,province_id,district_id,customer,supplier,linea_credito]
        print(columns)
        for c,cell in enumerate(columns):
            ws.write(r+1,c,cell)

    wb.save("{}_{}.xls".format(name_file,int(time.time())))

def download_partner(name_file,limit=10):
    with open("{}_{}.csv".format(name_file,int(time.time())), mode='w') as partner_csv:
        partner_writer = csv.writer(partner_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fields = ["id","type","name","catalog_06_id","vat","company_type","estado_contribuyente",
                    "registration_name","street","mobile","email","zip","country_id",
                    "state_id","province_id","district_id","customer","supplier","linea_credito",
                    "employee","parent_id","function","phone"]
        kwargs = {"fields":fields}
        if limit>0:
            kwargs.update({"limit":limit})
        partners = conn.call_kw("res.partner","search_read",[[]],kwargs)

        partner_writer.writerow(fields)
        for partner in partners:
            idx = partner["id"] if partner["id"] else ""
            tipo = partner["type"] if partner["type"] else ""
            name = partner["name"] if partner["name"] else ""
            if partner["catalog_06_id"]:
                catalog_06_id = str(partner["catalog_06_id"][0])
            else:
                catalog_06_id = "-"
            vat = partner["vat"] if partner["vat"] else ""
            company_type = partner["company_type"] if partner["company_type"] else ""
            estado_contribuyente = partner["estado_contribuyente"] if partner["estado_contribuyente"] else ""
            registration_name = partner["registration_name"] if partner["registration_name"] else ""
            street = partner["street"] if partner["street"] else ""
            mobile = partner["mobile"] if partner["mobile"] else ""
            email = partner["email"] if partner["email"] else ""
            ubigeo = partner["zip"] if partner["zip"] else ""
            country_id = str(partner["country_id"][1] if partner["country_id"] else "")
            state_id = str(partner["state_id"][1] if partner["state_id"] else "")
            province_id = str(partner["province_id"][1] if partner["province_id"] else "")
            district_id = str(partner["district_id"][1] if partner["district_id"] else "")
            customer = str(partner["customer"])
            supplier = str(partner["supplier"])
            linea_credito = str(partner["linea_credito"])
            employee = str(partner["employee"])
            parent_id = partner["parent_id"][1] if partner["parent_id"] else ""
            function = str(partner["function"])
            phone = str(partner["phone"])
            
            row = [idx,tipo,name,catalog_06_id,vat,company_type,estado_contribuyente,
                    registration_name,street,mobile,email,ubigeo,country_id,
                    state_id,province_id,district_id,customer,supplier,linea_credito,
                    employee,parent_id,function,phone]

            partner_writer.writerow(row)
"""

conn = Odoo("IW94Do1PeS_db","admin","adm1n*2019-11","erp.highlandtc.com",True)
conn.authenticate()

lista = conn.call_kw("res.partner","search_read",kwargs={"domain":['|',["active","=",0],["active","=",1]],
                                                        "fields":["name","active"]} ) 

print([x for x in lista if x["active"]])