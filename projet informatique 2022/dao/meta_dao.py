from business_object.generation_donnee import Generation_donnee
from business_object.regle_generation.meta_type import Meta_type
from business_object.regle_generation.typ import Type
from dao.db_connection import DBConnection
from utils.singleton import Singleton
from factory.meta_factory import MetaFactory

class MetaDao : 
    """
        Classe permettant de manipuler la table meta_type stockée en base de données.
        Méthodes find, save, update et delete avec différents paramètres
    """
    def find_all_meta(self):
        metas=[]
        liste_metas = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "SELECT * FROM meta_type"
                )
                res = cursor.fetchall()
                for row in res:
                    if row['nom_meta_type'] not in metas:
                        metas.append(row['nom_meta_type'])
        for nom_meta in metas:
            meta = MetaFactory().get_meta_type_from_sql_query(res, nom_meta)
            liste_metas.append(meta)
        return liste_metas
    
    def save_meta(self, meta : Meta_type):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                for tip in meta.list_type :
                    cursor.execute(
                        "INSERT INTO meta_type(nom_meta_type, nom_type) "+ 
                        "VALUES ( %(nom_meta_type)s, %(nom_type)s) "
                    , {"nom_meta_type" : meta.nom,
                        "nom_type":tip})

    def find_ids_meta(self, nom_meta : str):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                ids =[]
                cursor.execute(
                    "SELECT * FROM meta_type "+
                    "WHERE nom_meta_type = %(nom_meta_type)s ",
                    {"nom_meta_type" : nom_meta}                    
                )
                res = cursor.fetchall()
                for row in res:
                    ids.append(row['id_meta_type'])
        return ids
 

    def delete_meta_by_name(self, nom_meta_type : str):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "DELETE FROM meta_type "+
                    "WHERE nom_meta_type = %(nom_meta)s",
                    {"nom_meta" : nom_meta_type}
                )    

    def find_meta_by_name(self, nom_meta : str):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "SELECT * FROM meta_type "+
                    "WHERE nom_meta_type=%(nom_meta)s "
                    , {"nom_meta" : nom_meta})
                res = cursor.fetchall()
                mt = MetaFactory.get_meta_type_from_sql_query(res, nom_meta)
        return mt

    def delete_all_meta_type(self):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute("DELETE FROM meta_type ; "+
                               "ALTER SEQUENCE id_meta_type_seq RESTART WITH 1")

    def delete_doublons(self):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "DELETE FROM meta_type as m "+
                    "USING meta_type as m2 "+
                    "WHERE m.id_meta_type > m2.id_meta_type "+
                    "and m.nom_meta_type = m2.nom_meta_type "+
                    "and m.nom_type = m2.nom_type "
                )



if __name__ == '__main__':
    print('Tests de la classe MetaDao en commentaires')

    ##Test de find_all_meta
    #metas = MetaDao().find_all_meta()
    #print(len(metas) == 2)

    ##Test de "save_meta"
    #meta1 = Meta_type(
    #    nom = 'meta_test',
    #    list_type = ['prénom', 'code postal'])
    #MetaDao().save_meta(meta1)

    ##Test de find_ids_meta
    #ids = MetaDao().find_ids_meta(nom_meta = 'meta_test')
    #print(ids)

    ##Test de delete_meta_by_name
    #MetaDao().delete_meta_by_name('meta_test')

    ##Test de find_meta_by_name
    #meta = MetaDao().find_meta_by_name('commune')
    #print(meta.nom, meta.list_type)
