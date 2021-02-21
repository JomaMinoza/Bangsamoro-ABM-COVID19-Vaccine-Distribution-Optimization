def get_localized_death(location):
    def total_deaths(model):
        total = 0
        for agent in model.get_localized_agents(location):
            if agent.is_dead():
                total += 1
        return total
    return total_deaths
