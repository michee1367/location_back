
from middlewares.Middleware import Middleware, PROP_NAME_MIDDLEWARE_ACTION
from  enums.MiddlewareType import MiddlewareType
from services.middlewares.MiddlewareDTO import MiddlewareDTO

def add_model_middleware_action(cls, cls_middleware, name, *args, **kwargs) :
        try :
            # Vérifier que cls_middleware est bien une classe
            if not isinstance(cls_middleware, type):
                return cls  # On ignore, mais on ne casse pas la classe
            
            # Vérifier qu'il hérite de Middleware ET qu'il est de type ACTION
            if not (issubclass(cls_middleware, Middleware) 
                    and cls_middleware.check(*args, **kwargs)) :
                return cls   # On ignore
            
            middleware = cls_middleware(*args, **kwargs)
            
            
            if not (middleware.getType() == MiddlewareType.ACTION) :
                return cls
            
            # Ajouter la liste si absente
            if not hasattr(cls, PROP_NAME_MIDDLEWARE_ACTION):
                setattr(cls, PROP_NAME_MIDDLEWARE_ACTION, [])
                
            att_value = getattr(cls, PROP_NAME_MIDDLEWARE_ACTION)
            
            att_value.append(
                MiddlewareDTO(name, cls.__tablename__, cls, cls_middleware(*args, **kwargs))
            )
            
            #print(att_value)
        except Exception as e :
            print("Middleware : " + str(e))
            
def middleware_list_to_dict(middlewares: list) :
    return [dto.getResume() for dto in middlewares if isinstance(dto, MiddlewareDTO)]