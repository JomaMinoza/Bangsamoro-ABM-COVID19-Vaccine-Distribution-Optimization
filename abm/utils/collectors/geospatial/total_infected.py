from abm.models.enum.severity import Severity

def get_localized_infected(location):
    def total_infected(model):
        total = 0
        for agent in model.get_localized_agents(location):
            if agent.is_infected():
                if agent.severity != Severity.Exposed:
                    total += 1
        return total
    return total_infected
