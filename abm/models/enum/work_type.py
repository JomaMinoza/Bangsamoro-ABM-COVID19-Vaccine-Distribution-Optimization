from enum import Enum

class WorkType(str, Enum):
    Household = 'h'
    Frontliner = 'f'
    Teacher = 't'
    Private = 'p'
