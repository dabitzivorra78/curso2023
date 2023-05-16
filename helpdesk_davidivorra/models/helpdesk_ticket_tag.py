from odoo import api, fields, models

class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'
    _description = 'Helpdesk Ticket Tag'

    # Nombre
    name = fields.Char(
        required=True
    )
    ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket',
        relation='helpdesk_ticket_tag_rel',
        column1='tag_id',
        column2='ticket_id',
        string='Tickets')
    
    @api.model
    def _clean_tags(self):
        self.search([('ticket_ids', '=', False)]).unlink()

