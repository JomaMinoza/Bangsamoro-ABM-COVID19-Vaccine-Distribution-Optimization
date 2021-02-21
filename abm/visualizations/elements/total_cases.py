from mesa.visualization.modules import TextElement

class TotalCases(TextElement):

    def __init__(self):
        pass

    def render(self, model):
        return "Total Cases: %s"%(model.total_cases)
