from abm.models.enum.severity import Severity

def total_infected(model):
    total = 0
    for agent in model.schedule.agents:
        if agent.is_infected():
            if agent.severity != Severity.Exposed:
                total += 1
    return total
