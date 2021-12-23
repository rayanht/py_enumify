from ast import unparse
import io
import unittest

from py_enumify import load_ast_from_stringIO, transform_ast

class PyEnumifyTestCases(unittest.TestCase):
    def test_1(self):
        test_str = """test_dict = {
    "Rayan": 0,
    "Kevin": 1,
    "Maria": 2,
    "Mike": 3,
    "Julia": 4}"""
        expected = """class TestDict(Enum):
    RAYAN = 0
    KEVIN = 1
    MARIA = 2
    MIKE = 3
    JULIA = 4"""
        with io.StringIO() as f:
            f.write(test_str)
            f.seek(0)
            self.assertEqual(expected, unparse(transform_ast(load_ast_from_stringIO(f))))

    def test_2(self):
        test_str = \
        """x = random.randint(0, 10)\ntest_dict = {'Rayan': x, 'Kevin': 1, 'Maria': 2, 'Mike': 3, 'Julia': 4}"""
        with io.StringIO() as f:
            f.write(test_str)
            f.seek(0)
            self.assertEqual(test_str, unparse(transform_ast(load_ast_from_stringIO(f))))

    def test_3(self):
        test_str = \
        """x = 2\ntest_dict = {'Rayan': x, 'Kevin': 1, 'Maria': 2, 'Mike': 3, 'Julia': 4}"""
        with io.StringIO() as f:
            f.write(test_str)
            f.seek(0)
            self.assertEqual(test_str, unparse(transform_ast(load_ast_from_stringIO(f))))