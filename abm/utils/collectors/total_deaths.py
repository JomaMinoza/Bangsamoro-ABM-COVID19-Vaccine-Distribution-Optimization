def total_deaths(model):
    total = 0
    for agent in model.schedule.agents:
        if agent.is_dead():
            total += 1
    return total
