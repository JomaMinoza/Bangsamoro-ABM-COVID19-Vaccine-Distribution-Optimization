from abm.space.geospace.base import BaseGeoSpace
from abm.visualizations.modules.MapModule import MapModule

from mesa.datacollection import DataCollector

from abm.models.enum.age_group import AgeGroup

from abm.utils.collectors.geospatial.total_susceptible import get_localized_susceptible
from abm.utils.collectors.geospatial.total_exposed import get_localized_exposed
from abm.utils.collectors.geospatial.total_infected import get_localized_infected
from abm.utils.collectors.geospatial.total_deaths import get_localized_death
from abm.utils.collectors.geospatial.total_recovered import get_localized_recovered
from abm.utils.collectors.geospatial.total_vaccinated import get_localized_vaccinated
from abm.utils.collectors.geospatial.total_vaccinated_age_group import get_localized_vaccine_distribution

from abm.utils.modules.optimization.vaccine_distribution_optimization import vaccine_distribution_optimization
from abm.utils.modules.json_updater import json_updater

from abm.visualizations.charts.summary import SummaryChartModule
from abm.visualizations.charts.distribution import DistributionChartModule
from abm.visualizations.elements.label import Label
from abm.visualizations.portrayals.geospatial import agent_portrayal

import numpy as np
import pandas as pd
import json

class GeoSpaceEnvironment:

    def __init__(self, model, geojson_file, geojson_feature_key, locations, center_coords, population, data_manager, location_filter, vaccine_prioritization_weights, vaccines_available = 1000, scale = 1000):
        self.model                  = model
        self.geo_space              = BaseGeoSpace(model, geojson_file, geojson_feature_key, len(locations))
        self.center_coords          = center_coords
        self.locations              = locations
        self.population             = population
        self.data_manager           = data_manager
        self.map                    = self.get_map()
        self.agent_locations        = self.get_geospace().agents
        self.data                   = []
        self.infection_rates        = self.data_manager.get_updated_data("INFECTION_RATE")
        self.mortality_rates        = self.data_manager.get_updated_data("MORTALITY_RATE")
        self.vaccine_prioritization_weights = vaccine_prioritization_weights
        self.vaccines_available     = vaccines_available
        self.sub_problems           = []
        self.scale                  = scale
        self.vaccine_distribution   = {}
        self.population_distribution = {}
        self.susceptible_matrix     = np.empty((0, 9))
        
        self.localized_data_collectors          =  []
        self.localized_distribution_collectors  =  []
        self.localized_summaries                =  []
        self.localized_labels                   =  []
        self.localized_distribution_summaries   =  []
        self.localized_distribution_labels      =  []
        
        self.initialized_data()
        self.populate_data(self.get_data_source(), location_filter)
                    
        self.get_susceptible_matrix()
        self.get_localized_data_collectors()
        self.get_localized_distribution_collectors()
        self.get_localized_labels_and_summaries()
            
    def get_geospace(self):
        return self.geo_space
    
    def get_data_source(self):
        return self.data_manager.get_data()
    
    def get_map(self, zoom = 7, width = 960, height = 480):
        return MapModule(
            portrayal_method = agent_portrayal,
            view = self.center_coords,
            zoom = zoom,
            map_height = height,
            map_width = width
        )
    
    def get_susceptible_matrix(self, vaccinate_young = True):
        for idx, agent in enumerate(self.data):
            age_group = 8
            if vaccinate_young:
                age_group += 1
                
            loc = np.empty(age_group, dtype=float)        
            susceptibles = self.data[idx]["SUSCEPTIBLE_AGENTS"]
            cnt = 0
            for i, susceptible in enumerate(susceptibles):
                if not (i == 0 and vaccinate_young == False):
                    loc[cnt] = self.data[idx]["SUSCEPTIBLE_AGENTS"][susceptible]["value"]
                    cnt += 1
            
            self.susceptible_matrix = np.append(self.susceptible_matrix, np.array([loc]), axis=0) 
                    
    def reset_susceptible_matrix(self, vaccinate_young = True):
        age_group = 8
        if vaccinate_young:
            age_group += 1
        
        self.susceptible_matrix = np.empty((0, age_group))
                
    def initialized_data(self):
        print("Initializing the data ...")
        for idx, agent in enumerate(self.agent_locations):
            self.data.append(
                {
                    "LOCATION_NAME": repr(agent),
                    "POPULATION": self.population[idx],
                    "DATA": {
                        "susceptible": 0,
                        "exposed": 0,
                        "infected": 0,
                        "recovered": 0,
                        "dead": 0
                    },
                    "VACCINE_ALLOCATION": {
                        "age_00-09": {
                            "min": 0,
                            "max": 9,
                            "value": 0
                        },
                        "age_10-19": {
                            "min": 10,
                            "max": 19,
                            "value": 0
                        },
                        "age_20-29": {
                            "min": 20,
                            "max": 29,
                            "value": 0
                        },
                        "age_30-39": {
                            "min": 30,
                            "max": 39,
                            "value": 0
                        },
                        "age_40-49": {
                            "min": 40,
                            "max": 49,
                            "value": 0
                        },
                        "age_50-59": {
                            "min": 50,
                            "max": 59,
                            "value": 0
                        },
                        "age_60-69": {
                            "min": 60,
                            "max": 69,
                            "value": 0
                        },
                        "age_70-79": {
                            "min": 70,
                            "max": 79,
                            "value": 0
                        },
                        "age_80-up": {
                            "min": 80,
                            "max": 100,
                            "value": 0
                        }                    
                    },
                    "SUSCEPTIBLE_AGENTS": {
                        "age_00-09": {
                            "min": 0,
                            "max": 9,
                            "value": 0
                        },
                        "age_10-19": {
                            "min": 10,
                            "max": 19,
                            "value": 0
                        },
                        "age_20-29": {
                            "min": 20,
                            "max": 29,
                            "value": 0
                        },
                        "age_30-39": {
                            "min": 30,
                            "max": 39,
                            "value": 0
                        },
                        "age_40-49": {
                            "min": 40,
                            "max": 49,
                            "value": 0
                        },
                        "age_50-59": {
                            "min": 50,
                            "max": 59,
                            "value": 0
                        },
                        "age_60-69": {
                            "min": 60,
                            "max": 69,
                            "value": 0
                        },
                        "age_70-79": {
                            "min": 70,
                            "max": 79,
                            "value": 0
                        },
                        "age_80-up": {
                            "min": 80,
                            "max": 100,
                            "value": 0
                        }                    
                    }
                }
            )
            
    def populate_data(self, dataframe, filter_field):
        for agent, location in enumerate(self.data):
            self.populate_raw_data(agent, filter_field, self.locations[agent])
            
        json_updater(self.data_manager.parameters_json_file, "LOCATION_DATA", self.data)

    def populate_raw_data(self, agent, filter_field, filter_value):
        population  = self.data[agent]["POPULATION"]
        agent_data = self.data_manager.update_location_based_parameters(population, filter_field, filter_value)
        self.data[agent]["DATA"] = agent_data
        return True
    
    def update_data(self, vaccinate_young = True):
        json_updater(self.data_manager.parameters_json_file, "LOCATION_DATA", self.data)
        self.reset_susceptible_matrix(vaccinate_young)
        self.get_susceptible_matrix(vaccinate_young)
        self.initialize_vaccination_scheme(vaccinate_young)
        
    def get_localized_data_collector(self, location):
        return DataCollector(
             model_reporters = {
                "Susceptible":  get_localized_susceptible(location),
                "Exposed":      get_localized_exposed(location),
                "Infected":     get_localized_infected(location),
                "Deaths":       get_localized_death(location),
                "Recovered":    get_localized_recovered(location),
                "Vaccinated":   get_localized_vaccinated(location)
            })

    def get_localized_distribution_collector(self, location):
        return DataCollector(
             model_reporters = {
                "0 - 9":            get_localized_vaccine_distribution(location, AgeGroup.A00to09),
                "10 - 19":          get_localized_vaccine_distribution(location, AgeGroup.A10to19),
                "20 - 29":          get_localized_vaccine_distribution(location, AgeGroup.A20to29),
                "30 - 39":          get_localized_vaccine_distribution(location, AgeGroup.A30to39),
                "40 - 49":          get_localized_vaccine_distribution(location, AgeGroup.A40to49),
                "50 - 59":          get_localized_vaccine_distribution(location, AgeGroup.A50to59),
                "60 - 69":          get_localized_vaccine_distribution(location, AgeGroup.A60to69),
                "70 - 79":          get_localized_vaccine_distribution(location, AgeGroup.A70to79),
                "80 and above":     get_localized_vaccine_distribution(location, AgeGroup.A80toXX)              
            })
        
    def get_localized_data_collectors(self):
        for shape_idx, agent in enumerate(self.agent_locations, start = 1):
            location = "loc_" + str(shape_idx)
            self.localized_data_collectors.append(self.get_localized_data_collector(location))

    def get_localized_distribution_collectors(self):
        for shape_idx, agent in enumerate(self.agent_locations, start = 1):
            location = "loc_" + str(shape_idx)
            self.localized_distribution_collectors.append(self.get_localized_distribution_collector(location))

    def get_localized_labels_and_summaries(self):
        for idx, agent in enumerate(self.agent_locations, start = 1):
            location = "loc_" + str(idx)
            summary_content = {
                "Susceptible":  get_localized_susceptible(location),
                "Exposed":      get_localized_exposed(location),
                "Infected":     get_localized_infected(location),
                "Deaths":       get_localized_death(location),
                "Recovered":    get_localized_recovered(location),
                "Vaccinated":   get_localized_vaccinated(location)
            }                
            
            self.localized_labels.append(Label(label = repr(agent), content = summary_content))
            
            self.localized_summaries.append(SummaryChartModule(
                canvas_width    = 900, 
                canvas_height   = 420, 
                data_collector  = "localized_data_collectors", 
                geospatial      = True, 
                location_index  = idx - 1))
                        
            self.localized_distribution_summaries.append(DistributionChartModule(
                canvas_width    = 825, 
                canvas_height   = 360, 
                data_collector  = "localized_distribution_collectors", 
                geospatial      = True, 
                location_index  = idx - 1))

            self.localized_distribution_labels.append(Label(label = "Vaccine Allocation for {0}".format(repr(agent))))
            
    def recalculate_susceptible_agents(self, agent, environment_agents):
        self.data[agent]["SUSCEPTIBLE_AGENTS"] = environment_agents
        
    def update_infection_rates(self):
        self.infection_rates = self.data_manager.update_infection_rate()
        return True
    
    def update_mortality_rates(self):
        self.mortality_rates = self.data_manager.update_mortality_rate()
        return True    
    
    def initialize_sub_problems(self, activated_weights):
        self.sub_problems    = []
        for weights in activated_weights:
            if activated_weights[weights]:
                self.sub_problems.append(self.vaccine_prioritization_weights[weights])
        
    
    def initialize_vaccination_scheme(self, vaccinate_young = True):
        self.reset_susceptible_matrix(vaccinate_young)
        self.get_susceptible_matrix(vaccinate_young)        
        
        susceptible_population = np.matrix(self.susceptible_matrix).T
        
        available_vaccines     = self.vaccines_available
        sub_problems           = self.sub_problems
        
        result = vaccine_distribution_optimization(susceptible_population, available_vaccines,  sub_problems = sub_problems)
        result_json = json.loads(result)
                
        return result_json
    
    def update_vaccine_allocation(self, vaccinate_young = True):
        optimization_results = self.initialize_vaccination_scheme(vaccinate_young)        
        self.data_manager.update_vaccine_allocation(optimization_results, vaccinate_young)
        self.data    = self.data_manager.get_updated_data("LOCATION_DATA")
    
    def get_summary_plots(self):
        return True
