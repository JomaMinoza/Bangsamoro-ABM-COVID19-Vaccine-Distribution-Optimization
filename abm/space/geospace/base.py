from mesa_geo.geospace import GeoSpace
from mesa_geo.geoagent import AgentCreator

from abm.space.geoagents.base import BaseGeoAgent
from shapely.geometry import Point
import random

class BaseGeoSpace(GeoSpace):

    def __init__(self, model, geojson_file, geojson_feature_key, nlocations):
        super().__init__()
        self.model = model
        self.locations = self.instantiate_agents(geojson_file, geojson_feature_key, nlocations)

    def instantiate_agents(self, geojson_file, geojson_feature_key, nlocations):
        agent_creator = AgentCreator(
            BaseGeoAgent,
            {"model": self.model})

        agents = agent_creator.from_file(
            geojson_file,
            unique_id = geojson_feature_key)
        
        self.add_agents(agents)

        return dict([("loc_" + str(i+1), agents[i]) for i in range(nlocations)])

    def random_position(self, location):
        polygon = self.locations[location].shape
        x_min, y_min, x_max, y_max = polygon.bounds

        random_position = ()
        flag = True
        while flag:
            random_position = (random.uniform(x_min, x_max), random.uniform(y_min, y_max))
            
            if polygon.contains(Point(random_position[0], random_position[1])):
                flag = False

        return random_position
    

