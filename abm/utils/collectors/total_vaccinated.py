def total_vaccinated(model):
    total = 0
    for agent in model.schedule.agents:
        if agent.is_vaccinated():
            total += 1
    return total
