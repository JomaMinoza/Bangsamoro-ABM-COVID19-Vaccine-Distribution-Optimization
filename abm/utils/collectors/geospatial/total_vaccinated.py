def get_localized_vaccinated(location):
    def total_vaccinated(model):
        total = 0
        for agent in model.get_localized_agents(location):
            if agent.is_vaccinated():
                total += 1
        return total
    return total_vaccinated
