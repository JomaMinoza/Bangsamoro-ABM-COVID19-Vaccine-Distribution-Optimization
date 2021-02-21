from mesa.visualization.modules import TextElement

class ActiveCases(TextElement):

    def __init__(self):
        pass

    def render(self, model):
        return "Active Cases: %s"%(model.active_cases)
