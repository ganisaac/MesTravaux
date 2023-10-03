from business_object.generation_donnee import Generation_donnee


class DataFactory():
    """
        classe ayant pour role de gérer la conversion
        des donnees brutes en dictionnaires de données convenable 
    """
    @staticmethod
    def get_data_from_sql_query(res):
        dat = {'id_donnee' : res['id_donnee'], 
                'nom_meta_type' : res['nom_meta_type'], 
                'nom_type' : res['nom_type'], 
                'order_donnee' : res['order_donnee'], 
                'value_donnee' : res['value_donnee']}
        return dat