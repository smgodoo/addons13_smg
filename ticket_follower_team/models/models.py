# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TicketTeam(models.Model):
    _inherit = ['helpdesk.team']

    follower_team = fields.Many2many('res.partner')


class HelpdeskTicket(models.Model):
    _inherit = ['helpdesk.ticket']

    @api.model
    def create(self, val):
        """
            TDE: Add follower to ticket when create ticket
            To complete this, we need to add follower to team at Configure menu --> Ticket team
         """
        ticket = super(HelpdeskTicket, self).create(val)
        partner_ids = []
        if ticket.team_id:
            followers = [follower.id for follower in ticket.team_id.follower_team]
            partner_ids.extend(followers)
        if partner_ids:
            ticket.message_subscribe(partner_ids=partner_ids)
        return ticket
