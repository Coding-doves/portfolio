from enum import Enum


class UserRole(str, Enum):
    root = "root"
    admin = "admin"
    
    
class LearningModeEnum(str, Enum):
    remote = "remote"
    in_person = "in-person"
    hybrid = "hybrid"
