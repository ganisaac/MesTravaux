from business_object.regle_generation.typ import Type
from dao.db_connection import DBConnection
from utils.singleton import Singleton
from factory.typ_factory import TypeFactory

class TypeDao:
    """
        Classe permettant de manipuler la table type stockée en base de données.
        Méthodes find, save, update et delete avec différents paramètres
    """
    def find_all_type(self):
        typs=[]
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "SELECT * from type"
                )
                res = cursor.fetchall()
                for row in res: 
                    typ = TypeFactory.get_type_from_sql_query(row)
                    typs.append(typ)
        return typs
    
    def find_type_by_id(self, id : int):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                   "SELECT * FROM type WHERE id_type = %(id)s LIMIT 1"
                   , { "id" : id}
                )
                res = cursor.fetchone()
                typ = TypeFactory.get_type_from_sql_query(res)
                return typ

    def save_type(self,type:Type):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "INSERT INTO type(tx_remplissage, nom) VALUES "+
                    "(%(tx_remplissage)s, %(nom)s)"
                    , {"tx_remplissage" : type.tx_remplissage, 
                       "nom" : type.nom}
                )

    def find_type(self, type:Type):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "SELECT * FROM type WHERE nom = %(nom_type)s AND tx_remplissage = %(tx_remplissage)s"
                    , {"nom_type" : type.nom,
                        "tx_remplissage": type.tx_remplissage}
                        )
                res = cursor.fetchone()
                typ = TypeFactory.get_type_from_sql_query(res)
                return typ
    
    def update_type_by_id(self, id : int, new_type:Type):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "UPDATE type "+
                    "SET tx_remplissage = %(tx_remplissage)s, nom = %(nom)s " +
                    " where id_type = %(id_type)s",
                    {"id_type" : id,"tx_remplissage": new_type.tx_remplissage, "nom" : new_type.nom}
                )
                
    def delete_type(self,type:Type):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "DELETE FROM type "+
                    " WHERE id_type IN ( "+
                    "SELECT id_type FROM type "+
                    "WHERE nom = %(nom)s AND tx_remplissage = %(tx_remplissage)s " +
                    "LIMIT 1 )",
                    {"nom":type.nom, 
                    "tx_remplissage" : type.tx_remplissage}
                )

    def find_id_type(self, type:Type):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "SELECT id_type from type "+
                    "WHERE nom = %(nom)s AND tx_remplissage = %(tx_remplissage)s ",
                    {"nom":type.nom, 
                    "tx_remplissage" : type.tx_remplissage}                    
                )
                res = cursor.fetchone()
                return res['id_type']

    def delete_type_by_id(self,id_type:int):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "DELETE FROM type "+
                    " where id_type = %(id)s",
                    {"id":id_type}
                )

    def delete_all_type(self):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute("DELETE FROM type ; "+
                               "ALTER SEQUENCE id_type_seq RESTART WITH 1")

    def delete_doublons(self):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "DELETE FROM type as m "+
                    "USING type as m2 "+
                    "WHERE m.id_type > m2.id_type "+
                    "and m.nom = m2.nom "+
                    "and m.tx_remplissage = m2.tx_remplissage "
                )


if __name__ == "__main__":
    print("Tests de la DAO concernant la classe Type en commentaires")
    ##Test find_all_type
    #types = TypeDao().find_all_type()
    #print(len(types) == 2)
#
    ##Test find_type_by_id
    #type1 = TypeDao().find_type_by_id(2)
    #print(type1.nom, type1.tx_remplissage)
#
    ##Test save_type
    #type2 = Type(nom = 'âge',
    #             tx_remplissage = 1)
    #TypeDao().save_type(type2)
#
    ##Test find_type
    #type3 = TypeDao().find_type(type1)
    #print(type3)
    #print(type3.nom, type3.tx_remplissage)
#
    ##Test update_type
    #type4 = Type(0.8, "tranche d'âge")
    #TypeDao().update_type_by_id(id=3, new_type= type4) 
#
    ###Test delete_type
    #TypeDao().delete_type(type4)
    #
    ##Test find_id_type : 
    #type5 = Type(1, "adresse")
    #TypeDao().save_type(type5)
    #res = TypeDao().find_id_type(type5)
    #print(res)    
    #
    ##Test delete_type_by_id
    #type6 = Type(0.5, "email")
    #TypeDao().save_type(type6)
    #res = TypeDao().find_id_type(type6)
    #TypeDao().delete_type_by_id(id_type = res)
