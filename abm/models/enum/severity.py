from enum import Enum

class Severity(str, Enum):
    Zero = 'n'
    Exposed = 'e'
    Asymptomatic = 'a'
    Mild = 'm'
    Critical = 'c'