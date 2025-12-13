from enum import Enum


class UserRole(Enum):
    USER= "USER"
    STAFF= "STAFF"
    DG = "DG"
    MANAGER = "MANAGER"
    IT = "IT"
    LOGISTICS = "LOGISTICS"
    MAINTENANCE = "MAINTENANCE"
    AUDITOR = "AUDITOR"