from abm.models.enum import severity
from abm.models.enum.status import Status
from abm.models.enum.severity import Severity

def count_age_status(model, min_age, max_age, status, **kwargs):
    count = 0    
    severity = kwargs.get("severity", Severity.Mild)
        
    for agent in model.get_agents(min_age, max_age):
        if agent.get_status() == status:
            if status == Status.Infected:
                if agent.severity == severity:
                    count += 1
            else:
                count += 1
                
    return count
