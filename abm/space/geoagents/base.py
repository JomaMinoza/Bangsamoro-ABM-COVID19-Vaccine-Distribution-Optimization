from mesa_geo import GeoAgent

class BaseGeoAgent(GeoAgent):
    def __init__(self, unique_id, model, shape):
        super().__init__(unique_id, model, shape)
        self.location = unique_id
        
    def __repr__(self):
        return str(self.unique_id)
