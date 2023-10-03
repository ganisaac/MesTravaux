from dao.db_connection import DBConnection
import unittest
from dao.modality_dao import ModalityDao 
from business_object.regle_generation.modality import Modality

class TestModalityDao(unittest.TestCase):

    def test_find_all_modality(self):
        modality_dao = ModalityDao()
        mods = modality_dao.find_all_modality()
        self.assertEqual(8, len(mods))

    def test_find_modality_by_id(self):
        mod = ModalityDao().find_modality_by_id(id = 1)
        mod1 = Modality(nom_type='sexe',
                        proba_apparition = 0.5,
                        value='femme')
        self.assertEqual(mod.value, mod1.value)
        self.assertEqual(mod.proba_apparition, mod1.proba_apparition)
        self.assertEqual(mod.nom_type, mod1.nom_type)

if __name__ == "__main__":
    unittest.main()
