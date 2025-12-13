MIDDLEWARE_ENTITIES_CLASSES = []



def init_middlewares_entities(app):
    with app.app_context():
        if not hasattr(app, 'middlewares_entities'):
            app.middlewares_entities = {}
            
        if not hasattr(app, 'models_middlewares_entities_mapping'):
            app.models_middlewares_entities_mapping = {}

        # Enregistre tous les services déclarés avec @service
        for cls in MIDDLEWARE_ENTITIES_CLASSES:
            instance = cls._register_service()
            print(f"middleware model enregistré : {cls.__name__} -> {instance}")