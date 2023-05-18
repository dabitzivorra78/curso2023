
# Copyright <2023> David Ivorra - divorra78@gmail.com
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Helpdesk David Ivorra",
    "summary": "Gestiona incidencias",
    "version": "16.0.1.0.0",
    "category": "Helpdesk",
    "website": "https://totmaterial.es",
    "author": "totmaterial, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",        
        "views/helpdesk_ticket_action_views.xml",
        "views/helpdesk_ticket_views.xml",
        "views/helpdesk_ticket_tag_views.xml",
        "data/helpdesk_cron.xml",
    ],
}