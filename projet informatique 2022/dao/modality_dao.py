from business_object.regle_generation.modality import Modality
from dao.db_connection import DBConnection
from utils.singleton import Singleton
from factory.modality_factory import ModalityFactory
from utils.singleton import Singleton

class ModalityDao(metaclass=Singleton):
    """
        Classe permettant de manipuler la table modality stockée en base de données.
        Méthodes find, save, update et delete avec différents paramètres
    """
    def find_all_modality(self):
        mods=[]
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "SELECT * from modality"
                )
                res = cursor.fetchall()
                for row in res: 
                    mod = ModalityFactory().get_modality_from_sql_query(row)
                    mods.append(mod)
        return mods
    
    def find_modality_by_id(self, id : int):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                   "SELECT * FROM modality WHERE id_modality = %(id)s"
                   , { "id" : id}
                )
                res = cursor.fetchone()
                modality = ModalityFactory().get_modality_from_sql_query(res)
                return modality

    def find_modality(self, modality:Modality, limit: int=None):
        mods = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "SELECT * from modality " +
                    "WHERE nom_type = %(nom)s AND value = %(value)s "+
                    "ORDER BY nom_type, value "+
                    "LIMIT %(limit)s"
                    , {"nom" : modality.nom_type,
                       "value" : modality.value,
                       "limit" : limit
                       }
                    )
                res = cursor.fetchall()
                for row in res: 
                    mod = ModalityFactory().get_modality_from_sql_query(row)
                    mods.append(mod)
        return mods

    def save_modality(self,modality:Modality):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "INSERT INTO modality(nom_type, value, proba_apparition) VALUES "+
                    "(%(nom_type)s, %(value)s, %(proba)s)"
                    , {"nom_type" : modality.nom_type,
                       "value" : modality.value, 
                       "proba" : modality.proba_apparition }
                )
     
    def update_modality_by_id(self, id : int, new_type : str, new_value : str, new_proba_apparition : float):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE modality " +
                    "SET nom_type = %(type)s, value = %(value)s, proba_apparition = %(proba)s " +
                    "WHERE id_modality = %(id)s",
                    {"type" : new_type,
                     "value" : new_value,
                     "proba" : new_proba_apparition,
                     "id" : id}
                )

    def delete_modality_by_id(self, id):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "DELETE FROM modality "+
                    "WHERE id_modality = %(id)s "
                    , {"id" : id}
                )

    def delete_modality_by_mod(self,modality:Modality):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "DELETE FROM modality "+
                    "WHERE nom_type = %(nom)s AND value = %(value)s AND proba_apparition = %(proba)s "
                    , {"nom" : modality.nom_type,
                       "value" : modality.value,
                       "proba" : modality.proba_apparition}
                )

    def delete_modality_by_type(self, nom_type):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "DELETE FROM modality "+
                    "WHERE nom_type = %(nom)s  "
                    , {"nom" : nom_type}
                )

    def delete_doublons(self):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "DELETE FROM modality as m "+
                    "USING modality as m2 "+
                    "WHERE m.id_modality > m2.id_modality "+
                    "and m.nom_type = m2.nom_type "+
                    "and m.value = m2.value "
                )

    def delete_all_modality(self):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute("DELETE FROM modality ; "+
                               "ALTER SEQUENCE id_modality_seq RESTART WITH 1")


if __name__ == "__main__":
    print("Tests de la classe ModalityDao en commentaires")
    ##Test find_all_modality
    #modality = ModalityDao().find_all_modality()
    #print(len(modality) == 8)

    ##Test find_modality_by_id
    #mod1 = ModalityDao().find_modality_by_id(3)
    #print(mod1.nom_type, mod1.proba_apparition, mod1.value)

    ##Test save_modality
    #mod2 = Modality(nom_type = 'prénom',
    #                proba_apparition=0,
    #                value = "Nathan")
    #ModalityDao().save_modality(mod2)

    ##Test find_modality
    #mod3 = ModalityDao().find_modality(mod2, limit=1)
    #print(mod3)
    #for mod in mod3:
    #    print(mod.nom_type, mod.proba_apparition, mod.value)

    ##Test update_modality
    #ModalityDao().update_modality_by_id(id=5, new_type = 'prénom', new_value = 'Nathan', new_proba_apparition = 0) 

    ##Test delete_modality_by_mod
    #ModalityDao().delete_modality_by_mod(mod2)
    
    ##Test delete_doublons
    #ModalityDao().delete_doublons()

    ##Test delete_modality_by_type
    #ModalityDao().delete_modality_by_type("nom")
