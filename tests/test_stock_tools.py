# This file is part of the stock_tools module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class StockToolsTestCase(ModuleTestCase):
    'Test Stock Tools module'
    module = 'stock_tools'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        StockToolsTestCase))
    return suite
