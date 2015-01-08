#This file is part stock_tools module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import Pool
from .shipment import *

def register():
    Pool.register(
        ShipmentOutTool,
        module='stock_tools', type_='model')
