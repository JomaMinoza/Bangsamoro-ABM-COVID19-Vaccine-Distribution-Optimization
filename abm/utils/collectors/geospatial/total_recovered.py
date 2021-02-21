def get_localized_recovered(location):
    def total_recovered(model):
        total = 0
        for agent in model.get_localized_agents(location):
            if agent.is_recovered():
                total += 1
        return total
    return total_recovered
