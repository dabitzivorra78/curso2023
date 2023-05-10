from odoo import fields, models

class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = 'Helpdesk Ticket Action'

    # Nombre
    name = fields.Char(
        required=True
    )
    state = fields.Selection(
        selection=[
            ('todo', 'To Do'),
            ('done', 'Done'),
        ],
        default='todo'
    )
    ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket',
        string='ticket')

    def set_done(self):       
        self.write({'state': "done"})
    def set_todo(self):       
        self.write({'state': "todo"})