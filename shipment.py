#This file is part stock_tools module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool
from trytond.pyson import Eval, Not, Equal
from trytond.transaction import Transaction

__all__ = ['ShipmentOutTool']


class ShipmentOutTool(ModelSQL, ModelView):
    'Shipment Out Tool'
    __name__ = 'stock.shipment.out.tool'
    shipment = fields.Many2One('stock.shipment.out', 'Shipment', required=True,
        states={
            'readonly': Not(Equal(Eval('state'), 'draft')),
            }, depends=['state'])
    shipment_date = fields.Date('Date', readonly=True)
    customer = fields.Many2One('party.party', 'Customer',
        required=True)
    delivery_address = fields.Many2One('party.address', 'Delivery Address',
        required=True)
    warehouse = fields.Many2One('stock.location', "Warehouse",
        required=True, domain=[('type', '=', 'warehouse')])
    employee = fields.Many2One('company.employee', 'Employee')
    moves = fields.Function(fields.One2Many('stock.move', None, 'Moves',
        depends=['shipment']), 'on_change_with_moves')
    outgoing_moves = fields.Function(fields.One2Many('stock.move', None, 'Incoming Moves',
        depends=['shipment']), 'on_change_with_outgoing_moves')
    inventory_moves = fields.Function(fields.One2Many('stock.move', None, 'Inventory Moves',
        depends=['shipment']), 'on_change_with_inventory_moves')
    state = fields.Function(fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
        ('assigned', 'Assigned'),
        ('packed', 'Packed'),
        ('waiting', 'Waiting'),
        ], 'State'), 'get_state')

    @classmethod
    def __setup__(cls):
        super(ShipmentOutTool, cls).__setup__()
        cls._order.insert(0, ('shipment_date', 'DESC'))
        cls._order.insert(1, ('id', 'DESC'))
        cls._buttons.update({
                'next': {},
                })

    @staticmethod
    def default_state():
        return 'draft'

    @staticmethod
    def default_employee():
        User = Pool().get('res.user')
        if Transaction().context.get('employee'):
            return Transaction().context['employee']
        else:
            user = User(Transaction().user)
            if user.employee:
                return user.employee.id

    @fields.depends('shipment')
    def on_change_shipment(self):
        changes = {}
        if self.shipment:
            changes['customer'] = self.shipment.customer.id
            changes['delivery_address'] = self.shipment.delivery_address.id
            changes['warehouse'] = self.shipment.warehouse.id
            changes['state'] = self.shipment.state
        return changes

    @fields.depends('shipment')
    def on_change_with_moves(self, name=None):
        return [move.id for move in self.shipment.moves]

    @fields.depends('shipment')
    def on_change_with_outgoing_moves(self, name=None):
        return [move.id for move in self.shipment.moves if (move.from_location.id == self.shipment.warehouse.output_location.id)]

    @fields.depends('shipment')
    def on_change_with_inventory_moves(self, name=None):
        return [move.id for move in self.shipment.moves if (move.to_location.id == self.shipment.warehouse.output_location.id)]

    def get_state(self, name):
        if self.shipment:
            return self.shipment.state
        else:
            return 'draft'

    @classmethod
    def set_shipment_date(cls, tools):
        Date = Pool().get('ir.date')
        cls.write(tools, {
                'shipment_date': Date.today(),
                })

    @classmethod
    def create(cls, vlist):
        tools = super(ShipmentOutTool, cls).create(vlist)
        cls.set_shipment_date(tools)
        return tools

    @classmethod
    @ModelView.button
    def next(cls, tools):
        for tool in tools:
            method_name = 'next_%s' % tool.shipment.state
            if hasattr(cls, method_name):
                getattr(cls, method_name)(tool)
        return 'new'

    def next_draft(self):
        pool = Pool()
        Shipment = Pool().get('stock.shipment.out')

        # Change new state: waiting
        Shipment.wait([self.shipment])

    def next_waiting(self):
        pool = Pool()
        Shipment = Pool().get('stock.shipment.out')

        # Change new state: assigned
        Shipment.assign_try([self.shipment])

    def next_assigned(self):
        pool = Pool()
        Shipment = Pool().get('stock.shipment.out')

        # Change new state: assigned
        Shipment.pack([self.shipment])

    def next_packed(self):
        pool = Pool()
        Shipment = Pool().get('stock.shipment.out')

        # Change new state: done
        Shipment.done([self.shipment])
