from business_object.regle_generation.typ import Type
from business_object.regle_generation.modality import Modality
import unittest


class TestModality(unittest.TestCase):

    def test_add_modality(self):
        m = Modality("age", 100, 22)
        t = Type(100, "age")
        t.add_type()
        m2 = m.add_modality()
        self.assertEqual(m2, {1: {'type': 'age', 'value': 22, "proba d'apparition": 100}})

    def test_delete_modality(self):
        m3 = Modality.delete_modality("age", 22)
        self.assertEqual(m3, {1: {'type': 'age', 'value': 22, "proba d'apparition": 0}})




if __name__ == '__main__':
    unittest.main()


