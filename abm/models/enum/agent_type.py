from enum import Enum

class AgentType(str, Enum):
    Person = 'p'
    House = 'h'
    Market = 'm'
    School = 's'
    Business = 'b'
