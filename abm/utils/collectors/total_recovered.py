def total_recovered(model):
    total = 0
    for agent in model.schedule.agents:
        if agent.is_recovered():
            total += 1
    return total
