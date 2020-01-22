
1. Crear entorno virtual python
virtualenv -p

Cargar Traduccióm Spanish(MX)

Cambiar login

#Creación de movimientos contables de Facturas  
invoices = self.env['account.invoice'].search([['state','in',['open','paid']],['number','=',False]])
for idx,inv in enumerate(invoices):
    print(idx)
    state = inv.state
    inv.action_date_assign()
    inv.action_move_create()
    inv.state = state
    self.env.cr.commit()
    