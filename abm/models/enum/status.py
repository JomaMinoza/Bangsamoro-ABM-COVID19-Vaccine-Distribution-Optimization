from enum import Enum

class Status(str, Enum):
    Susceptible = 's'
    Infected = 'i'
    Vaccinated = 'v'
    Recovered = 'r'
    Dead = 'd'
    
