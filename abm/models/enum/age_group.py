from enum import Enum

class AgeGroup(int, Enum):
    A00to09 = 0
    A10to19 = 1
    A20to29 = 2
    A30to39 = 3
    A40to49 = 4
    A50to59 = 5
    A60to69 = 6
    A70to79 = 7
    A80toXX = 8