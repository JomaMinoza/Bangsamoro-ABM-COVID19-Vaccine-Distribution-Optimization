def total_susceptible(model):
    total = 0
    for agent in model.schedule.agents:
        if agent.is_susceptible():
            total += 1
    return total
