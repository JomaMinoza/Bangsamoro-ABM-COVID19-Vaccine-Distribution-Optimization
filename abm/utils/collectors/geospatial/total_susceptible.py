def get_localized_susceptible(location):
    def total_susceptible(model):
        total = 0
        for agent in model.get_localized_agents(location):
            if agent.is_susceptible():
                total += 1
        return total
    return total_susceptible
