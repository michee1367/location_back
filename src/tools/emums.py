from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

def get_enums_from_model(model_class):
    enums = {}
    for column in model_class.__table__.columns:
        if isinstance(column.type, (Enum, PgEnum)):
            enum_class = column.type.enum_class
            enums[column.name] = [e.name for e in enum_class]
    return enums
