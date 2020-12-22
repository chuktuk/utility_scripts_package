#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


import unittest
from utility_scripts import dash_tools

from pandas import DataFrame
import dash_bootstrap_components as dbc
import dash_table

# define a test dataframe
test_df = DataFrame({'strings': ['this', 'column', 'contains', 'strings'],
                     'integers': [1, 10, 100, 1000],
                     'floats': [2.2, 20.20, 200.200, 99.999999]})


class TestDashDFInit(unittest.TestCase):
    def setUp(self):
        self.dff = dash_tools.DashDF(test_df)

    def test_dash_df_init(self):
        """Ensure dash dataframe is a different object than the original dataframe."""
        # create a dash dataframe
        self.assertNotEqual(id(test_df), id(self.dff))
        self.assertIsInstance(self.dff, dash_tools.DashDF)
        self.assertRaises(ValueError, dash_tools.DashDF, 'not a df')


class TestConversions(unittest.TestCase):
    def setUp(self):
        self.dff = dash_tools.DashDF(test_df)

    def test_convert_currency_result(self):
        self.dff.convert_currency('integers')
        self.assertListEqual(list(self.dff['integers']), ['$1.00', '$10.00', '$100.00', '$1,000.00'])

    def test_convert_percent_result(self):
        self.dff.convert_percent('floats')
        self.assertListEqual(list(self.dff['floats']), ['2.20 %', '20.20 %', '200.20 %', '100.00 %'])

    def test_currency_on_strings(self):
        self.assertRaises(ValueError, self.dff.convert_currency, 'strings')

    def test_percent_on_strings(self):
        self.assertRaises(ValueError, self.dff.convert_percent, 'strings')

    def test_currency_key_error(self):
        self.assertRaises(KeyError, self.dff.convert_currency, 'doesntexist')

    def test_percent_key_error(self):
        self.assertRaises(KeyError, self.dff.convert_percent, 'doesntexist')

    def test_column_name_types(self):
        self.assertRaises(TypeError, self.dff.convert_currency, 1)

    def test_column_name_types2(self):
        self.assertRaises(TypeError, self.dff.convert_percent, 1)


class TestFormattedDashTable(unittest.TestCase):
    def setUp(self):
        self.dff = dash_tools.DashDF(test_df)
        self.table = self.dff.get_formatted_dash_table()
        self.props = self.table.to_plotly_json()

    def test_get_formatted_dash_table(self):
        self.assertIsInstance(self.table, dbc.Table)
        self.assertIsInstance(self.props, dict)


class TestInteractiveDashTable(unittest.TestCase):
    def setUp(self):
        self.dff = dash_tools.DashDF(test_df)
        self.table = self.dff.get_interactive_dash_table()

    def test_get_interactive_dash_table(self):
        self.assertIsInstance(self.table, dash_table.DataTable)
        data = self.table.data
        self.assertListEqual(data, [{'strings': 'this', 'integers': 1, 'floats': 2.2},
                                    {'strings': 'column', 'integers': 10, 'floats': 20.20},
                                    {'strings': 'contains', 'integers': 100, 'floats': 200.200},
                                    {'strings': 'strings', 'integers': 1000, 'floats': 99.999999}])


class TestDashStyles(unittest.TestCase):
    def setUp(self):
        self.styles = dash_tools.DashStyles()

    def test_dash_styles(self):
        self.assertIsInstance(self.styles, dash_tools.DashStyles)

    def test_accessing_card_text_style(self):
        self.assertEqual(self.styles.dash_card_text, {'textAlign': 'center', 'color': '#0074D9'})

    def test_dash_styles_repr(self):
        self.assertEqual(self.styles.__repr__, 'Custom css styles for dash app.')


class TestCreateCard(unittest.TestCase):
    def setUp(self):
        self.card = dash_tools.create_card('card title',
                                           'test-id',
                                           'test-card-id',
                                           color='primary',
                                           outline=True,
                                           inverse=True)
        self.props = self.card.to_plotly_json()['props']

    def test_create_card_instance(self):
        self.assertIsInstance(self.card, dbc.Card)
        self.assertIsInstance(self.props, dict)

    def test_card_attributes(self):
        self.assertEqual(self.props['id'], 'test-card-id')
        self.assertTrue(self.props['inverse'])


class TestDashFigure(unittest.TestCase):
    def setUp(self):
        self.figure = dash_tools.make_dash_figure(None, None, 'figure-id', 6)

    def test_make_dash_figure(self):
        self.assertIsInstance(self.figure, dbc.Col)
        self.assertIsInstance(self.figure.children, dbc.Tabs)


if __name__ == '__main__':
    unittest.main()
