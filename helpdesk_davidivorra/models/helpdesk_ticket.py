from odoo import api, Command,fields, models
from odoo.exceptions import UserError 
from datetime import timedelta

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
    
    @api.model
    def _get_default_date(self):
        return fields.Date.today()
    
    # Fecha
    date = fields.Date(
        default=_get_default_date,
    )
    
    # Fecha y hora limite
    date_limit = fields.Datetime(
        string='Limit Date & Time',
        #compute='_compute_date_limit',
        #inverse='_inverse_date_limit',
        #store=True
        )
    
    #@api.depends('date')
    #def _compute_date_limit(self):
    #    for record in self:
    #        if record.date:
    #            record.date_limit = record.date + timedelta(days=1)
    #        else:
    #            record.date_limit = False
    #def _inverse_date_limit(self):
    #    pass
    
    #Añadir un onchange para que al indicar la fecha ponga como fecha de vencimiento un día mas

    @api.onchange('date')
    def _onchange_date(self):
            if self.date:
                self.date_limit = self.date + timedelta(days=1)
            else:
                 self.date_limit = False

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
        relation='helpdesk_ticket_tag_rel',
        column1='ticket_id',
        column2='tag_id',
        string='Tags')
    action_ids = fields.One2many(
        comodel_name='helpdesk.ticket.action',
        inverse_name='ticket_id',
        string='Actions')

    def set_actions_as_done(self):
        self.ensure_one()
        self.action_ids.set_done()

    color = fields.Integer('Color Index', default=0)

    person_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[('is_company', '=', False)],
    )
    amount_time = fields.Float(
        string="Amount of time")
    
    #- Añadir una restricción para hacer que el campo time no sea menor que 0

    @api.constrains('amount_time')
    def _chek_amount_time(self):
        for record in self:
            if record.amount_time <0:
                raise UserError( ("The amount of time can't be negative"))

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
    
    #Modificar el botón de crear una etiqueta en el formulario de ticket para que abra una acción nueva, 
    #pasando por contexto el valor del nombre y la relación con el ticket.
    def create_tag(self):
        self.ensure_one()
        #self.write({'tag_ids' : [(0,0,{'name': self.tag_name})]})     
        #self.write({'tag_ids' : [Command.create({'name': self.tag_name})]})
       #action = self.env["ir.actions.actions"]._for_xml_id("helpdesk_davidivorra.helpdesk_ticket_tag_action")
        action ={
            'name': 'Helpdesk Tickets Tags',
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.ticket.tag',
        }     
        action['context'] = {
            'default_name': self.tag_name,
            'default_ticket_id': self.id,    
        }
        action['view_mode'] = 'form'
        action['binding_view_types'] = 'form'
        action['target'] = 'new'
        return action

    def clear_tags(self):
        self.ensure_one()
        tag_ids = self.env['helpdesk.ticket.tag'].search([('name', '=', 'otra')])
        
        #self.write({'tag_ids' : [
        #    (5,0,0),
        #    (6,0,tag_ids.ids)]})  

        self.tag_ids =[
            Command.clear(),
            Command.set(tag_ids.ids)]
        
    def get_related_actions(self):
        self.ensure_one()
        #action = self.env["ir.actions.actions"]._for_xml_id("helpdesk_davidivorra.helpdesk_ticket_action_related_action")
        #return action
        action = self.env["ir.actions.actions"]._for_xml_id("helpdesk_davidivorra.helpdesk_ticket_action_action")
        action['domain'] = [('ticket_id','=',self.id)]
        action['context'] = {'default_ticket_id': self.id}
        return action
        
    def get_assigned(self):
        self.ensure_one()
        self.state ='assigned'
        self.user_id = self.env.user

       # import pdb; pdb.set_trace()
       # self.tag_ids = [
       #     Command.clear(),
       #     Command.set(tag_ids.ids)]

