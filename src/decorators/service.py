from flask import current_app
from models import db
def middleware_entity(name, models):
    """
    Décorateur pour enregistrer une instance unique (singleton)
    dans current_app.middlewares_entities, avec des attributs optionnels.
    
    Exemple :
        @middleware_entity(name="user_service", models=[Asset, Location])
        class UserService:
            ...
    """
    def decorator(cls):
        def register():
            # Initialise le conteneur des middlewares_entities si nécessaire
            if not hasattr(current_app, 'middlewares_entities'):
                current_app.middlewares_entities = {}
            if not hasattr(current_app, 'models_middlewares_entities_mapping'):
                current_app.models_middlewares_entities_mapping = {}

            # Crée l’instance unique
            instance = cls()

            # Stocke l’instance sous le nom fourni ou le nom de la classe
            service_name = name or cls.__name__
            current_app.middlewares_entities[service_name] = instance

            # Injecte les attributs personnalisés comme métadonnées
            models_middlewares_entities_mapping = current_app.models_middlewares_entities_mapping
            for model in models:
                if not issubclass(model, db.Model) :
                    continue
                
                tablename = model.__tablename__
                
                if not models_middlewares_entities_mapping.get(tablename, None) :
                    models_middlewares_entities_mapping[tablename] = []
                    
                models_middlewares_entities_mapping[tablename].append(instance)
                
                #setattr(instance, key, value)

            return instance

        cls._register_service = register
        cls._service_name = name or cls.__name__
        cls._service_attrs = models
        
        return cls

    return decorator
