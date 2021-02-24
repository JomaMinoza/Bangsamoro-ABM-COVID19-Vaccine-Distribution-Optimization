from abm.models.agents.geospatial.person import Person
from abm.space.geoagents.base import BaseGeoAgent

from abm.models.enum.viral_load import ViralLoad
from abm.models.enum.severity import Severity

def agent_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {}
    
    if isinstance(agent, Person):
        portrayal = {
            "radius":                           "1",
            "Shape":                            "Circle", 
            "Age":                              int(agent.age),
            "Viral Load":                       agent.viral_load.name,
            "Severity":                         agent.severity.name,
            "Status":                           agent.status.name,
            "Wearing Masks":                    agent.facemask,
            "Physical Distance":                agent.distance,
            "Immunity":                         agent.immunity,
            "In Quarantine":                    agent.in_quarantine,
            "In Lockdown":                      agent.in_lockdown,
            "Vaccine Hesistancy":               agent.vaccine_hesitant,
            "Time Infected":                    agent.time_infected,
            "Recovery Time":                    agent.recovery_period,
            "Incubation Time":                  agent.incubation_period
        }

        if agent.is_susceptible():
            if agent.facemask:
                portrayal["color"] = "White"
            else:
                portrayal["color"] = "Brown"
                
        elif agent.is_infected():
            if agent.severity == Severity.Exposed:
                portrayal["color"] = "Orange"
            else:
                portrayal["color"] = "Red"
        elif agent.is_recovered():
            portrayal["color"] = "Green"
        elif agent.is_dead():
                portrayal["color"] = "Black"
        elif agent.is_vaccinated():
                portrayal["color"] = "Yellow"

    elif isinstance(agent, BaseGeoAgent):
        portrayal = { "color": "Blue" }

    return portrayal


