def count_status(model, status):
    count = 0
    for agent in model.schedule.agents:
        if agent.get_status() == status:
            count = count + 1
    return count
