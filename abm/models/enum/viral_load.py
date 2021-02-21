from enum import Enum

class ViralLoad(str, Enum):
    High = 'h'
    Medium = 'm'
    Low = 'l'
    Zero = 'z'