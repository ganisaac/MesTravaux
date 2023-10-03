from business_object.generation_donnee import Generation_donnee
from business_object.regle_generation.meta_type import Meta_type
from business_object.regle_generation.typ import Type
from dao.db_connection import DBConnection
from utils.singleton import Singleton
from factory.data_factory import DataFactory

class DataDao : 
    """
        Classe permettant de manipuler la table donnee stockée en base de données.
        Méthodes find, save, update et delete avec différents paramètres
    """    
    def find_all_data(self):
        data=[]
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "SELECT * FROM donnee"
                )
                res = cursor.fetchall()
                for row in res:
                    dat = DataFactory.get_data_from_sql_query(row)
                    data.append(dat)
        return data
    
    def save_data(self, nb_inv : int, nom_m : int, data : dict):  ### data = Generation_donnee.jeu_donnee
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                for key in list(data.keys())[-nb_inv::] : 
                    for i,tip in enumerate(data[key].keys()) :
                        cursor.execute(
                            "INSERT INTO donnee(nom_meta_type, nom_type, order_donnee, value_donnee)"+ 
                            "VALUES ( %(nom_meta)s, %(nom_type)s, %(order)s, %(value)s)"
                        , {"nom_meta" : nom_m,
                            "nom_type":tip,
                            "order" : i+1,
                            "value" : data[key][tip]})

    def find_data_by_id(self, id_donnee):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "SELECT * FROM donnee WHERE id_donnee=%(id_donnee)s "
                    , {"id_donnee" : id_donnee})
                res = cursor.fetchone()
        return res

    def find_data_by_meta(self, nom_meta : str):
        data=[]
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "SELECT * FROM donnee WHERE nom_meta_type=%(nom_meta)s "
                    , {"nom_meta" : nom_meta})
                res = cursor.fetchall()
                for row in res:
                    dat = DataFactory.get_data_from_sql_query(row)
                    data.append(dat)
        return data
    
    def find_row_data(self, nom_meta : str, i_row : int, nb_col : int): 
        data = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "SELECT id_donnee, nom_meta_type, nom_type, order_donnee, value_donnee "+
                    "FROM ( (SELECT MIN(id_donnee) as min FROM donnee WHERE nom_meta_type = %(nom_meta)s ) as tamp1 "+
                    "CROSS JOIN (SELECT * FROM donnee WHERE nom_meta_type = %(nom_meta)s) AS tamp2 ) AS tamp "+
                    "WHERE id_donnee >= min+%(n_col)s*(%(i_row)s-1) AND id_donnee<min+%(n_col)s*%(i_row)s"
                    , {"i_row" : i_row,
                        "n_col" : nb_col,
                        "nom_meta" : nom_meta})
                res = cursor.fetchall()
                for row in res:
                    dat = DataFactory.get_data_from_sql_query(row)
                    data.append(dat)
        return data
    
    def find_col_data(self, nom_meta : str, nom_type : str):
        data=[]
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "SELECT * FROM donnee WHERE nom_meta_type=%(nom_meta)s AND nom_type = %(nom_type)s "
                    , {"nom_meta" : nom_meta,
                        "nom_type" : nom_type})
                res = cursor.fetchall()
                for row in res:
                    dat = DataFactory.get_data_from_sql_query(row)
                    data.append(dat)
        return data

    def find_id_donnee(self, ligne:list):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "SELECT * FROM donnee "+
                    "WHERE nom_meta_type = %(nom_meta)s AND nom_type = %(nom_type)s AND order_donnee = %(order)s AND value_donnee = %(value)s",
                    {"nom_meta" : ligne[0],
                    "nom_type": ligne[1], 
                    "order" : ligne[2], 
                    "value" : ligne[3]}                    
                )
                res = cursor.fetchall()
                for row in res:
                    dat = DataFactory.get_data_from_sql_query(row)
                    data.append(dat['id_donnee'])
        return data

    def update_data_by_id(self, id : int, new_data:list):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "UPDATE donnee "+
                    "SET nom_meta_type = %(nom_meta)s, nom_type = %(nom_type)s, order_donnee = %(order)s, value_donnee = %(value)s " +
                    "WHERE id_donnee = %(id)s",
                    {"nom_meta" : new_data[0],
                    "nom_type": new_data[1], 
                    "order" : new_data[2], 
                    "value" : new_data[3],
                    "id": id}
                )
    
    def delete_row_data(self, nom_meta:str, nb_col : int, i_row : int):  
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "DELETE FROM donnee WHERE id_donnee IN ("+
                    "SELECT id_donnee "+
                    "FROM ( (SELECT MIN(id_donnee) as min FROM donnee WHERE nom_meta_type = %(nom_meta)s ) as tamp1 "+
                    "CROSS JOIN (SELECT * FROM donnee WHERE nom_meta_type = %(nom_meta)s) AS tamp2 ) AS tamp "+
                    "WHERE id_donnee >= min+%(n_col)s*(%(i_row)s-1) AND id_donnee<min+%(n_col)s*%(i_row)s)"
                    , {"i_row" : i_row,
                        "n_col" : nb_col,
                        "nom_meta" : nom_meta})

    def delete_data_by_id(self, id : int):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "DELETE FROM donnee "+
                    " WHERE id_donnee = %(id)s",
                    {"id" : id}
                )

    def delete_data_by_meta(self, nom_meta : str):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(
                    "DELETE FROM donnee "+
                    " WHERE nom_meta_type = %(nom_meta)s",
                    {"nom_meta" : nom_meta}
                )

    def delete_all_data(self):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute("DELETE FROM donnee ; "+
                               "ALTER SEQUENCE id_donnee_seq RESTART WITH 1")

if __name__ == "__main__" :
    dat = DataDao().find_row_data(nom_meta = "indiv",
                            i_row = 5,
                            nb_col = 2)
    print(dat)



    