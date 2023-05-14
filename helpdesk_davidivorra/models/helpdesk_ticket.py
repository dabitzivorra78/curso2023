from odoo import api, Command,fields, models
from odoo.exceptions import UserError 

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

    def set_actions_as_done(self):
        self.ensure_one()
        self.action_ids.set_done()

    color = fields.Integer('Color Index', default=0)

    amount_time = fields.Float(
        string="Amount of time")

        #Hacer que el campo assigned sea calculado, hacer que se pueda buscar con el atributo search y 
        #hacer que se pueda modificar de forma que si lo marco se actualice el usuario con el usuario conectado y 
        #si lo desmarco se limpie el campo del usuario.
    assigned = fields.Boolean(
        compute='_compute_assigned',
        search='_search_assigned',
        inverse='_inverse_assigned',
    )
    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            record.assigned = bool(record.user_id )

    def _search_assigned(self, operator, value):
        if operator not in ('=', '!=') or not isinstance(value, bool):
            raise UserError( ("Operation not supported"))
        if operator == '=' and value == True:
            operator = '!='
        else:
            operator = '='
        return [('user_id', operator, False)]

    def _inverse_assigned(self):
        for record in self:
            if not record.assigned:
                record.user_id = False
            else:
                record.user_id = self.env.user

    #hacer un campo calculado que indique, dentro de un tiquet, la cantidad de tiquets asociados al mismo usuario.
    tickets_count = fields.Integer(
        compute='_compute_tickets_count',
        string='Tickets count',
    )
    @api.depends('user_id')
    def _compute_tickets_count(self):
        ticket_obj = self.env['helpdesk.ticket']
        for record in self:
            tickets = ticket_obj.search([('user_id', '=', record.user_id.id)])
            record.tickets_count = len(tickets)
    #crear un campo nombre de etiqueta, y hacer un botón que cree la nueva etiqueta con ese nombre y lo asocie al ticket.
    tag_name = fields.Char()
    
    def create_tag(self):
        self.ensure_one()
        #self.write({'tag_ids' : [(0,0,{'name': self.tag_name})]})     
        #self.write({'tag_ids' : [Command.create({'name': self.tag_name})]})
        self.tag_ids = [Command.create({'name': self.tag_name})]
    def clear_tags(self):
        self.ensure_one()
        tag_ids = self.env['helpdesk.ticket.tag'].search([('name', '=', 'otra')])
        
        #self.write({'tag_ids' : [
        #    (5,0,0),
        #    (6,0,tag_ids.ids)]})  
        self.tag_ids = [
            Command.clear(),
            Command.set(tag_ids.ids)]

