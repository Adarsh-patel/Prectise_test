from odoo import api,models,fields,_
import re
from odoo.exceptions import ValidationError,UserError

class sample_purchase_order(models.Model):

    _inherit = "purchase.order.line"

    product_type = fields.Selection("Product Type",related="product_id.type")


class sample_sale_order(models.Model):

    _inherit = "sale.order"

    @api.depends('order_line.product_id')
    def _change_product(self):
        for rec in self.order_line:
            self.gross_weight += rec.product_id.weight
            print ("\n\nughefuwjhfei----->",rec.product_id.weight,self.gross_weight,"\n\n")

    @api.multi
    def action_wizard(self):
        ctx = dict(self.env.context)
        print ("\n\n Context------>",ctx)
        return {
            'name': _('open wizard'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order.line.wizard',
            'view_id': self.env.ref('Prectise.wizard_sale_order').id,
            'context':ctx,
            'type': 'ir.actions.act_window',
            'target': 'new'
        }

    @api.multi
    @api.depends('invoice_ids.state')
    def _get_invoice_status(self):
        # print("7tuygydhud9---------------------------------------   ")
        for order in self:
            if order.invoice_ids:
                for invoice in order.invoice_ids:
                    if invoice.origin == order.name:
                        if invoice.state == 'paid':
                            order.paid = 'paid'
                            # print("=---------------------------------")
                        else:
                            order.paid = 'unpaid'
            else:
                order.paid = 'unpaid'

    paid = fields.Char('invoice state',compute='_get_invoice_status',store=True)
    gross_weight = fields.Float("Gross weight", compute="_change_product")
    company_type = fields.Selection("company_type",related="partner_id.company_type")


class sale_order_wizard(models.TransientModel):

    _name = "sale.order.line.wizard"

    product_id = fields.Many2one('product.product','Product')
    qty = fields.Float('Quantity')
    price_unit = fields.Float('Unit price')

    @api.multi
    def action_save(self):
        for rec in self:
            active_id=rec._context.get('active_id')

            order_line = self.env['sale.order.line'].create({
                'product_id' : self.product_id.id,
                'product_uom_qty' : self.qty,
                'price_unit' : self.price_unit,
                'order_id' : active_id
            })

            print ("\n\norder_line------>",order_line)


class res_partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self,vals):
        seq = self.env['ir.sequence'].next_by_code('res.partner.seq')
        vals.update({'cust_seq':seq})
        res = super(res_partner, self).create(vals)
        return res

    @api.multi
    @api.onchange('email')
    def _check_email(self):
        if self.email:
            result = re.match('^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*@[a-zA-Z]+(.)+[a-zA-Z{2,4}]$', self.email)
            if result is None:
                raise ValidationError("Please enter email in valid formate e.g adarsh@gmail.com")

    cust_seq = fields.Char('Customer Sequence',readonly=True)



class account_invoice(models.Model):
    _inherit="account.invoice"

    @api.multi
    def unlink(self):
        for order in self:
            if order.amount_total > 10000:
                raise UserError(_('The invoice is not deleted because the invoice amount is grater than 10000.'))
        return super(account_invoice, self).unlink()


class Employee(models.Model):

    _inherit = "hr.employee"

    state = fields.Selection([('new','New'),('probation','Probation'),
                              ('confirmed','Confirmed'),('terminated','Terminated'),
                              ('resigned','Resigned')],default='new')
    @api.multi
    def action_new(self):
        self.state = 'new'

    @api.multi
    def action_probation(self):
        self.state = 'probation'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_terminated(self):
        self.state = 'terminated'

    @api.multi
    def action_resigned(self):
        self.state = 'resigned'


class res_partner_wizard(models.TransientModel):

    _name="res.partner.wizard"

    mobile = fields.Char("Mobile No",size=10)

    @api.multi
    def action_save_mobile(self):
        for rec in self:
            active_id = rec._context.get('active_id')
            print ("\n\n\n\nhello------------------->",self.mobile,active_id)

            data = self.env['res.partner'].browse(active_id)
            data.mobile = self.mobile
            print("\n\ndata=====================>",data)



