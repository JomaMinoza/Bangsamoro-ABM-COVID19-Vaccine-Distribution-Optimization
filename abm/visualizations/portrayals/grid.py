from abm.models.enum.status import Status
from abm.models.enum.viral_load import ViralLoad
from abm.models.enum.severity import Severity

from abm.resources.util import PERSON_ICONS

def agent_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {
        "Shape": PERSON_ICONS["SUSCEPTIBLE"], 
        "Layer": 0,
        "Age": int(agent.age),
        "Viral Load": agent.viral_load.name,
        "Severity": agent.severity.name,
        "Status": agent.status.name,
        "Wearing Masks": agent.facemask,
        "Physical Distance": agent.distance,
        "Immunity": agent.immunity,
        "In Quarantine Facility/Hospital": agent.in_quarantine,
        "In Lockdown": agent.in_lockdown
    }

    if agent.is_susceptible():
        portrayal["Color"] = ["#FF0000", "#FF9999"]
        portrayal["stroke_color"] = "#00FF00"
        portrayal["r"] = 0.1
        portrayal["Shape"] = PERSON_ICONS["SUSCEPTIBLE"]
    else:
        portrayal["Color"] = ["#0000FF", "#9999FF"]
        portrayal["stroke_color"] = "#000000"
        portrayal["r"] = 0.5
        portrayal["Shape"] = PERSON_ICONS["DIED"]

    portrayal["Time Infected"]   = agent.time_infected
    if agent.is_susceptible():
        if agent.facemask:
            portrayal["Shape"] = PERSON_ICONS["MASK"]
        else:
            portrayal["Shape"] = PERSON_ICONS["SUSCEPTIBLE"]
            
    elif agent.is_infected():
        if agent.viral_load == ViralLoad.High:
          portrayal["Shape"] = PERSON_ICONS["VIRAL"]
        elif agent.severity == Severity.Exposed:
          portrayal["Shape"] = PERSON_ICONS["EXPOSED"]
        else:
          portrayal["Shape"] = PERSON_ICONS["INFECTED"]
          
    elif agent.is_recovered():
        if agent.facemask:
            portrayal["Shape"] = PERSON_ICONS["MASK"]
        else:
            portrayal["Shape"] = PERSON_ICONS["RECOVERED"]
    elif agent.is_dead():
        portrayal["Shape"] = PERSON_ICONS["DIED"]
    elif agent.is_vaccinated():
        portrayal["Shape"] = PERSON_ICONS["VACCINATED"]

    return portrayal


