import numpy as np
import pandas as pd 
import json

from abm.resources.util import DATA_DROP_CSV_FILE
from abm.resources.util import QUEZON_CITY_DATA, QUEZON_CITY_DATA_LOC
from abm.resources.util import extract_data_drop_file

from abm.utils.modules.epi_data_extractor import epi_data_extractor
from abm.utils.modules.age_group_extractor import infection_age_group_values, case_fatality_age_group_values
from abm.utils.modules.optimization.vaccine_distribution_optimization import vaccine_distribution_optimization
from abm.utils.modules.json_updater import json_updater

pd.options.mode.chained_assignment = None

import os.path

class DataManager:
    
    def __init__(self, csv_file, parameters_json_file, filter_field, filter_value, age_distributions):
        self.csv_file               = csv_file
        self.parameters_json_file   = parameters_json_file
        self.input_parameters       = self.reload_data()
        self.age_distributions      = age_distributions
        
        if not os.path.isfile(csv_file):
            extract_data_drop_file()
            
        self.data           = self.get_data_from_csv_file()
        self.preprocessed(filter_field, filter_value)        
        
    def get_data_from_csv_file(self):
        return pd.read_csv(DATA_DROP_CSV_FILE, index_col = 0, low_memory = False)
    
    def get_data(self):
        return self.data
    
    def reload_data(self):
        return json.load(open(self.parameters_json_file))
        
    def get_updated_data(self, field):
        self.reload_data()
        return self.input_parameters[field]

    def preprocessed(self, filter_field, filter_value):
        data = self.data[['Age','AgeGroup','Sex','DateResultRelease','DateRecover','DateDied', 'RegionRes', 'ProvRes', 'CityMunRes','BarangayPSGC', 'RemovalType']]
        data['DateResultRelease'] = pd.to_datetime(data['DateResultRelease'])
        data['DateRecover']       = pd.to_datetime(data['DateRecover'])
        data['DateDied']          = pd.to_datetime(data['DateDied'])
        data                      = data[data[filter_field].isin(filter_value)]
        self.data                 = data
        
    def update_infection_rate(self):

        infection_age_group = infection_age_group_values(self.data)

        infection_rates = self.input_parameters["INFECTION_RATE"]
        rates           = []
        
        for index, rate in enumerate(infection_rates):
            infection_rates[rate]['rate']   =   infection_age_group[index] / self.age_distributions[index]
            rates.append(infection_rates[rate]['rate'])

        for index, rate in enumerate(infection_rates):
            infection_rates[rate]['rate']   =   infection_rates[rate]['rate'] / np.max(rates)

        json_updater(self.parameters_json_file, "INFECTION_RATE", infection_rates)
        
        return infection_rates

    def update_mortality_rate(self):

        case_fatality_age_group = case_fatality_age_group_values(self.data)

        mortality_rates = self.input_parameters["MORTALITY_RATE"]
        
        for index, mortality_rate in enumerate(mortality_rates):
            mortality_rates[mortality_rate]['rate'] = case_fatality_age_group[index] 

        json_updater(self.parameters_json_file, "MORTALITY_RATE", mortality_rates)
        
        return mortality_rates
        
    def update_location_based_parameters(self, population, filter_field, filter_value):
        epidemic_df = epi_data_extractor(self.data, filter_field, filter_value)
                
        infected        = epidemic_df['Case Incidence'].sum() / population
        recovered       = epidemic_df['Reported Recovered'].sum() / population
        dead            = epidemic_df['Reported Died'].sum() / population
        susceptible     = 1 - (infected + recovered + dead) 
        
        return {
                "susceptible": susceptible,
                "infected":    infected,
                "recovered":   recovered,
                "dead":        dead
        }
        
    def update_vaccine_allocation(self, optimization_results):
    
        location_distribution = pd.DataFrame(optimization_results["optimal_allocation_per_age"])
        location_distribution.index = ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80+"]
                
        locations_data         = self.input_parameters["LOCATION_DATA"]
        
        for idx, location in enumerate(locations_data):
            allocations = locations_data[idx]["VACCINE_ALLOCATION"]
            for jdx, allocation in enumerate(allocations):
                key = location_distribution.index[jdx]                
                locations_data[idx]["VACCINE_ALLOCATION"][allocation]["value"] = location_distribution.at[key, idx]
                
        json_updater(self.parameters_json_file, "LOCATION_DATA", locations_data)
                
            
