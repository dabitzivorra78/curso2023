from odoo import fields, models

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Helpdesk Ticket'
    
    
    # Nombre
    name = fields.Char(
        required=True,
        help="Resume brevemente en el título la incidencia"
    )
    
    # Descripción
    description = fields.Text(
        help="Detalla lo mejor posible la incidencia y como se produce.",
        default="Versión a la que afecta:     Modulo:    Pasos para el error:    Modulos personalizados:"
    )
    
    # Fecha
    date = fields.Date()
    
    # Fecha y hora limite
    date_limit = fields.Datetime(
        string='Limit Date &Time')
   
    # Asignado (Verdadero o Falso)
    assigned = fields.Boolean()
   
    # Acciones a realizar (Html)
    actions_todo = fields.Html()

