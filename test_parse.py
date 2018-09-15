"Test parse.py"
import unittest

import systems
import parse

from exceptions import MissingDelimiter


EXAMPLE_FULL = """
[a] > b @ 25
b > c @ 0.5
c > d @ 0.5, leak
d > [e] @ 1.0
"""


class TestParse(unittest.TestCase):
    def test_parse(self):
        model = parse.parse(EXAMPLE_FULL)
        stock_names = ['a', 'b', 'c', 'd', 'e']
        values = {
            'a': float('+inf'),
            'b': 0,
            'e': float('+inf'),
        }
        for stock_name in stock_names:
            stock = model.get_stock(stock_name)
            self.assertIsNotNone(stock)
            self.assertEqual(stock_name, stock.name)
            if stock_name in values:
                value = values[stock_name]
                self.assertEqual(value, stock.initial)

    def test_parse_missing_delim(self):
        txt = "[a] < b @ 25"
        with self.assertRaises(MissingDelimiter) as md:
            parse.parse(txt)
        self.assertEqual('>', md.exception.delimiter)

        txt = "[a] > b"
        with self.assertRaises(MissingDelimiter) as md:
            parse.parse(txt)
        self.assertEqual('@', md.exception.delimiter)            
        

        
        

if __name__ == "__main__":
    unittest.main()
