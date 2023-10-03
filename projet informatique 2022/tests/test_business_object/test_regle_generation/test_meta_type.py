from business_object.regle_generation.typ import Type
from business_object.regle_generation.meta_type import Meta_type
import unittest


class TestMetaType(unittest.TestCase):

    def test_add_meta_type(self):
        mt = Meta_type("individu", ["nom","age"])
        t1 = Type(100, "age")
        t2 = Type(100, "nom")
        t2.add_type()
        t1.add_type()
        mt1 = mt.add_meta_type()
        self.assertEqual(mt1, {'individu': ['nom', 'age']})

    def test_delete_meta_type(self):
        mt2 = Meta_type.delete_meta_type("individu")
        self.assertEqual(mt2, {})


if __name__ == '__main__':
    unittest.main()

