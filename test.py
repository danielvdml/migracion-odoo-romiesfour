from odoo import Odoo
import json

"""
conn1 = Odoo("5WI1q4kLj2_db","admin","admin","htc.facturacion.vip")
conn1.authenticate()
fields = ["id","name","cost_currency_id","currency_id"]

products = conn1.call_kw("product.template","search_read",kwargs={"fields":fields})

for x in products:
    print(x)

company = conn1.call_kw("res.company","search_read",kwargs={"fields":["name","currency_id"]})
print(company)
"""
#conn1 = Odoo("highlanddb_oct_final_migra","admin","admin","localhost:8827")
#conn1 = Odoo("5WI1q4kLj2_db","admin","admin","htc.facturacion.vip")

conn1 = Odoo("naomis_db_13_nov","yeyson5","Elbaronrojo5","localhost:8827")
conn1.authenticate()

productos = conn1.call_kw("product.product","search_read",kwargs={"fields":["id","name","categ_id","standard_price"]})
productos_dict = {}
for product in productos:
    productos_dict.update({product["id"]:[product["name"],product["categ_id"][1],product["standard_price"]]})

pos_orders = conn1.call_kw("pos.order","search_read",kwargs={"fields":["id",
                                                                    "partner_id",
                                                                    "invoice_id",
                                                                    "date_order",
                                                                    "amount_total",
                                                                    "lines"]})

records = []
for order in pos_orders:
    order_lines = conn1.call_kw("pos.order.line","search_read",
                                                kwargs={"fields":["name",
                                                                    "price_unit",
                                                                    "qty",
                                                                    "product_id",
                                                                    "price_subtotal",
                                                                    "discount",
                                                                    "salesman_id",
                                                                    "user_id"],
                                                        "domain":[["order_id","=",order["id"]]]})
    
    for line in order_lines:
        if productos_dict.get(line["product_id"][0],False):
            nombre_product,categoria_product,costo_product = productos_dict[line["product_id"][0]]
        else:
            nombre_product,categoria_product,costo_product = line["product_id"][1],"",0

        lines = [[str(order["id"]),
                    order.get("partner_id",False)[1] if order.get("partner_id",False) else "",
                    order.get("invoice_id",False)[1] if order.get("invoice_id",False) else "",
                    order["date_order"],
                    str(round(order["amount_total"],2)),
                    str(len(order_lines)),
                    nombre_product,
                    categoria_product,
                    str(round(costo_product,2)),
                    str(round(line["price_unit"],2)),
                    str(round(line["qty"],2)),
                    str(round(line["price_subtotal"],2)),
                    str(line["discount"])]]
        records +=  lines
#order_id;Cliente;Comprobante;Fecha de Orden;Monto;Cantidad de líneas;Producto;Categoria de Producto;Costo de Producto;Precio unitario;Cantidad;Subtotal;Descuento
f = open("pos_order_lines.csv","w")
for r  in records:
    print(r)
    f.write(";".join(r)+"\n")

f.close()