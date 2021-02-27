def get_localized_vaccine_distribution(location, age_group):
    def total_vaccinated(model):
        total = 0
        for agent in model.get_localized_agents(location):
            if agent.is_vaccinated() and agent.age_group == age_group:
                total += 1
        return total * model.environment.scale
    return total_vaccinated
