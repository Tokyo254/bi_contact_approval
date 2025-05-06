from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from lxml import etree

class ResPartner(models.Model):
    _inherit = 'res.partner'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Sales Approved'),
        ('approve2', 'Finance Approved')
    ], default='draft', tracking=True, string="Approval State")

    has_group = fields.Boolean(compute='_compute_has_group', store=False)

    @api.depends('active')
    def _compute_has_group(self):
        for rec in self:
            rec.has_group = rec.user_has_groups('bi_contact_approval.group_sales_administrator') or                             rec.user_has_groups('bi_contact_approval.group_finance_administrator')

    def button_draft(self):
        self.write({'state': 'draft'})

    def button_approve(self):
        self.write({'state': 'approve'})
        self._send_email_to_group('bi_contact_approval.email_template_contact_sales_approved', 'bi_contact_approval.group_finance_administrator')

    def button_approve2(self):
        self.write({'state': 'approve2'})
        self._send_email_to_group('bi_contact_approval.email_template_contact_finance_approved', 'base.group_system')

    def _send_email_to_group(self, template_ref, group_ref):
        template = self.env.ref(template_ref)
        group = self.env.ref(group_ref)
        emails = [user.email for user in group.users if user.email]
        if emails:
            template.with_context(lang=self.env.user.lang).sudo().send_mail(
                self.id,
                force_send=True,
                email_values={'email_to': ','.join(emails)}
            )

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type == 'form':
            doc = etree.XML(result['arch'])
            user = self.env.user
            is_editable = user.has_group('bi_contact_approval.group_sales_administrator') or user.has_group('bi_contact_approval.group_finance_administrator')
            if not is_editable:
                for node in doc.xpath("//field"):
                    node.set('readonly', 'state in ("approve","approve2")')
            result['arch'] = etree.tostring(doc, encoding='unicode')
        return result
