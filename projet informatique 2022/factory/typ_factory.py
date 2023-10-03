from business_object.regle_generation.typ import Type


class TypeFactory():
    """
        classe ayant pour role de gérer la conversion
        de donnees brutes en Type
    """
    @staticmethod
    def get_type_from_sql_query(res):
        ty = Type(
            tx_remplissage= res['tx_remplissage'],
            nom= res['nom'])
        #ty.id = int(res['id_type'])
        return ty