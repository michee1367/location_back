from middlewares.Middleware import Middleware


class MiddlewareDTO :
    
    def __init__(self, name, table_name, cls, middleware: Middleware) :
        
        self.name = name
        self.table_name = table_name
        self.cls = cls
        self.middleware = middleware
        
    def getResume(self) :
        return {
            "name": self.name,
            "table_name": self.table_name,
            "middleware": self.middleware.to_dict()
        }
        