import unittest
from business_object.regle_generation.typ import Type

class TestType(unittest.TestCase):

    def test_add_type(self):
        t = Type(100, "age")
        dic1 = t.add_type()
        self.assertEqual(dic1, {'age': {'remplissage': 100, 'id': 1}})

    def test_delete_type(self):
        dic2 = Type.delete_type("age")
        self.assertEqual(dic2, {})




if __name__ == '__main__':
    unittest.main()
