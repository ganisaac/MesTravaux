from business_object.regle_generation.meta_type import Meta_type


class MetaFactory():
    """
        classe ayant pour role de gérer la conversion
        de donnees brutes en Metatype
    """
    @staticmethod
    def get_meta_type_from_sql_query(res, nom_meta):
        types = []
        for row in res : 
            if row['nom_meta_type'] == nom_meta:
                types.append(row['nom_type'])   
        meta = Meta_type(
            nom = nom_meta,
            list_type = types)
        return meta