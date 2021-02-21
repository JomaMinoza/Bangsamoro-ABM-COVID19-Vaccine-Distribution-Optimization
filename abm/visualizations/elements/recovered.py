from mesa.visualization.modules import TextElement

class Recovered(TextElement):

    def __init__(self):
        pass

    def render(self, model):
        return "Recovered: %s"%(model.recovered)
