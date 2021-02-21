def agents_information(model):
    agents = []
    for agent in model.schedule.agents:
        agents.append(agent.get_information())