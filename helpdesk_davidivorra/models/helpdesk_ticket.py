from odoo import fields, models

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Helpdesk Ticket'
    
    
    # Nombre
    name = fields.Char(
        required=True,
        help="Resume brevemente en el título la incidencia"
    )
    
    # Secuencia
    sequence = fields.Integer(
            default=10,
            help="Contador para el orden de las incidencias"
    )
    # Descripción
    description = fields.Text(
        help="Detalla lo mejor posible la incidencia y como se produce.",
        default="""Versión a la que afecta:     
    Modulo:    
    Pasos para el error:    
    Modulos personalizados:
        """
    )
    
    # Fecha
    date = fields.Date()
    
    # Fecha y hora limite
    date_limit = fields.Datetime(
        string='Limit Date &Time')
   
    # Asignado (Verdadero o Falso)
    assigned = fields.Boolean(
        readonly=True,
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Assigned to"
    )
    # Acciones a realizar (Html)
    actions_todo = fields.Html()

    #Añadir el campo Estado [Nuevo, Asignado, En proceso, Pendiente, Resuelto, Cancelado], que por defecto sea Nuevo
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('assigned', 'Assigned'),
            ('in_progress', 'In Process'),
            ('pendind', 'Pending'),
            ('resolved', 'Resolved'),
            ('canceled', 'Canceled'),
        ],
        default='new',
    )
    
    def update_description(self):
        self.write({'name': "Descripción Revisada y Actualizada"})

    tag_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.tag',
        #relation='helpdesk_ticket_tag_rel',
        #column1='col_name',
        #column2='other_col_name',
        string='Tags')
    action_ids = fields.One2many(
        comodel_name='helpdesk.ticket.action',
        inverse_name='ticket_id',
        string='Actions')