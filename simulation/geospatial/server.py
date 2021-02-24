from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from abm.visualizations.elements.total_cases import TotalCases
from abm.visualizations.elements.active_cases import ActiveCases
from abm.visualizations.elements.recovered import Recovered

from abm.visualizations.inputs.sliders import *
from abm.visualizations.inputs.options import *
from abm.visualizations.inputs.checkboxes import *

import json
import os

from simulation.geospatial.model import GeoSimulationEnvironment
from abm.space.geospace import GeoSpaceEnvironment
from abm.space.geojson.constants import BARMM_GEOJSON

from abm.utils.modules import DataManager
from abm.resources.util import DATA_DROP_CSV_FILE, BARMM_DATA_LOC

PORT = os.environ.get('PORT', '8524')

simulation_model        = GeoSimulationEnvironment
center_coords           = [5.986803, 122.1695733]
locations               = ["BASILAN", "LANAO DEL SUR", "MAGUINDANAO", "SULU", "TAWI-TAWI"]
age_distributions       = [
                            1037200,   # 0 - 9 
                            931800,    # 10 - 19 
                            725000,    # 20 - 29 
                            629100,    # 30 - 39
                            453200,    # 40 - 49
                            296000,    # 50 - 59
                            173700,    # 60 - 69
                            68800,     # 70 - 79
                            15500      # 80 and up
                        ]

population              = [
                            385300,         # Basilan
                            1225700,        # Lanao Del Sur
                            1391100,        # Maguindanao
                            839500,         # Sulu
                            489100          # Tawi-Tawi
                        ]

vaccine_prioritization_weights = {
    "person_health_social_work":        [0.10, 0.32, 0.09, 0.37, 0.11],
    "person_prof_tech":                 [0.06, 0.37, 0.37, 0.12, 0.10],
    "person_admin_support":             [0.01, 0.75, 0.08, 0.10, 0.06],
    "person_education":                 [0.03, 0.77, 0.12, 0.04, 0.05],
    "person_agriculture":               [0.10, 0.75, 0.06, 0.06, 0.03],
    "elderly":                          [0.09, 0.28, 0.32, 0.19, 0.11],
    "social_household_4ps_active":      [0.066, 0.239, 0.306, 0.330, 0.059],
    "social_bayanihan_grant":           [0.08, 0.33, 0.31, 0.17, 0.11],
    "economics_tourists":               [0.1352, 0.1919, 0.3569, 0.0004, 0.3156],
    "economics_marine_fisheries":       [0.03, 0.23, 0.16, 0.13, 0.45],
    "economics_volume_fisheries":       [0.02, 0.02, 0.16, 0.36, 0.44],
    "economics_livestock_inventory":    [0.28, 0.31, 0.24, 0.10, 0.06],
    "economics_volume_corn":            [0.00009, 0.33832, 0.65840, 0.00129, 0.00189]
}

performance_factor       = 5
scale                    = 1000 * performance_factor  
vaccines_available       = 5000 / performance_factor # times scale (actual number for vaccine doses) 

data_manager            = DataManager(DATA_DROP_CSV_FILE, BARMM_DATA_LOC, "ProvRes", locations, age_distributions)
environment             = GeoSpaceEnvironment(simulation_model, BARMM_GEOJSON, "PROVINCE", locations, center_coords, population, data_manager, "ProvRes", vaccine_prioritization_weights, vaccines_available)
environment.scale       = scale

simulation_model.grid   = environment.get_geospace()

summary_plots           = environment.get_summary_plots()
total_cases_element     = TotalCases()
active_cases_element    = ActiveCases()
recovered_element       = Recovered()

components = [
    total_cases_element,
    active_cases_element,
    recovered_element,
    environment.map
]

for location in range(len(locations)):
    components.append(environment.localized_labels[location])
    components.append(environment.localized_summaries[location])
    components.append(environment.localized_distribution_labels[location])
    components.append(environment.localized_distribution_summaries[location])



model_params = {
    "model_desc":                   UserSettableParameter('static_text', value = "Model Parameters"),
    "scenarios":                    scenarios,
    "vaccination_implementation":   vaccination_implementation,   
    "vaccine_hesitancy":            vaccine_hesitancy,
    "vaccine_prior_lbl":            UserSettableParameter('static_text', value = "Vaccine Prioritization"),
    "person_health_social_work":    person_health_social_work_option,
    "person_prof_tech":             person_prof_tech_option,
    "person_admin_support":         person_admin_support_option,
    "person_education":             person_education_option,
    "person_agriculture":           person_agriculture_option,
    "elderly":                      elderly_option,
    "social_household_4ps_active":         social_household_4ps_active_option,
    "social_bayanihan_grant":              social_bayanihan_grant_option,
    "economics_tourists":                  economics_tourists_option,
    "economics_marine_fisheries":          economics_marine_fisheries_option,
    "economics_volume_fisheries":          economics_volume_fisheries_option,
    "economics_livestock_inventory":       economics_livestock_inventory_option,
    "economics_volume_corn":               economics_volume_corn_option,
    "epidemiology_lbl":             UserSettableParameter('static_text', value = "Epidemiology"),    
    "incubation_period":            incubation_period,
    "recovery_period":              recovery_period,
    "transmission_rate":            transmission_rate,  
    "viral_load_probability":       viral_load_probability,
    "behavioral_factors_lbl":       UserSettableParameter('static_text', value = "Behavioral Factors"),
    "wearing_masks":                wearing_masks,
    "social_distance_limit":        social_distance_limit,
    "health_factors_lbl":           UserSettableParameter('static_text', value = "Health Factors"),
    "natural_immunity":             natural_immunity,
    "exercise":                     exercise,
    "preexisting_conditions":       preexisting_conditions,
    "policy_lbl":                   UserSettableParameter('static_text', value = "Policy Restrictions"),
    "minority_restrictions":        minority_restrictions,
    "adult_restrictions":           adult_restrictions,   
    "environment":                  environment
}


server = ModularServer(
    simulation_model,
    components,
    "COVID19 Agent Based Model with Multi-Objective Optimization for Vaccine Distribution",
    model_params = model_params)

server.port = PORT
