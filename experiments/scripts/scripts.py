import os
import sys

import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.getcwd() + "/abm")
sys.path.insert(0, os.getcwd() + "/simulation/")
sys.path.insert(0, os.getcwd() + "/mesa/")



from mesa.batchrunner import BatchRunner

from simulation.grid.model import GridSimulationEnvironment

from abm.utils.collectors.total_susceptible import total_susceptible
from abm.utils.collectors.total_infected import total_infected
from abm.utils.collectors.total_deaths import total_deaths
from abm.utils.collectors.total_recovered import total_recovered
from abm.utils.collectors.total_vaccinated import total_vaccinated

from abm.utils.collectors.count_age_infected import *
from abm.utils.collectors.count_age_exposed import *
from abm.utils.collectors.count_age_died import *
from abm.utils.collectors.count_age_recovered import *

from abm.utils.collectors.count_peak_values import *

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 100)


warnings.simplefilter('ignore')


default_scenario_model_params = {
    "height": 200,
    "width": 200,
    "incubation_period": 7,
    "recovery_period": 14,
    "transmission_rate":  0.01,
    "viral_load_probability":  0.01,
    "wearing_masks": 0.8,
    "social_distance_limit": 0.7,
    "natural_immunity": 0.2,
    "exercise": 0.3,
    "preexisting_conditions": 0.6,
    "minority_restrictions": 21,
    "adult_restrictions": 60,
    "scenarios": "No Vaccination",
    "vaccination_implementation": "After 0 Days",
    "scale": 100,
}

default_vaccination_model_params = {
    "height": 200,
    "width": 200,
    "incubation_period": 7,
    "recovery_period": 14,
    "transmission_rate":  0.01,
    "viral_load_probability":  0.01,
    "wearing_masks": 0.8,
    "social_distance_limit": 0.7,
    "natural_immunity": 0.2,
    "exercise": 0.3,
    "preexisting_conditions": 0.6,
    "minority_restrictions": 21,
    "adult_restrictions": 60,
    "scenarios": "With Vaccination",
    "vaccination_implementation": "After 0 Days",
    "scale": 100,
}

mobility_vaccination_model_params = default_vaccination_model_params

mobility_vaccination_model_params["mobile_workforce"] = True

elderly_vaccination_model_params = default_vaccination_model_params

elderly_vaccination_model_params["elderly"] = True

all_configuration_vaccination_model_params = default_vaccination_model_params
all_configuration_vaccination_model_params["mobile_workforce"] = True
all_configuration_vaccination_model_params["elderly"] = True



variable_params = {"scale": range(100,100)}

model_reporters = {
    "Susceptible": total_susceptible,
    "Infected": total_infected,
    "Deaths": total_deaths,
    "Recovered": total_recovered,
    "Vaccinated": total_vaccinated,
    "Exposed: 0-9":   count_age_0_9_exposed,
    "Exposed: 10-19": count_age_10_19_exposed,
    "Exposed: 20-29": count_age_20_29_exposed,
    "Exposed: 30-39": count_age_30_39_exposed,
    "Exposed: 40-49": count_age_40_49_exposed,
    "Exposed: 50-59": count_age_50_59_exposed,
    "Exposed: 60-69": count_age_60_69_exposed,
    "Exposed: 70-79": count_age_70_79_exposed,
    "Exposed: 80+":   count_age_80_up_exposed,               
    "Infected: 0-9":   count_age_0_9_infected,
    "Infected: 10-19": count_age_10_19_infected,
    "Infected: 20-29": count_age_20_29_infected,
    "Infected: 30-39": count_age_30_39_infected,
    "Infected: 40-49": count_age_40_49_infected,
    "Infected: 50-59": count_age_50_59_infected,
    "Infected: 60-69": count_age_60_69_infected,
    "Infected: 70-79": count_age_70_79_infected,
    "Infected: 80+":   count_age_80_up_infected,
    "Died: 0-9":   count_age_0_9_died,
    "Died: 10-19": count_age_10_19_died,
    "Died: 20-29": count_age_20_29_died,
    "Died: 30-39": count_age_30_39_died,
    "Died: 40-49": count_age_40_49_died,
    "Died: 50-59": count_age_50_59_died,
    "Died: 60-69": count_age_60_69_died,
    "Died: 70-79": count_age_70_79_died,
    "Died: 80+":   count_age_80_up_died,
    "Recovered: 0-9":   count_age_0_9_recovered,
    "Recovered: 10-19": count_age_10_19_recovered,
    "Recovered: 20-29": count_age_20_29_recovered,
    "Recovered: 30-39": count_age_30_39_recovered,
    "Recovered: 40-49": count_age_40_49_recovered,
    "Recovered: 50-59": count_age_50_59_recovered,
    "Recovered: 60-69": count_age_60_69_recovered,
    "Recovered: 70-79": count_age_70_79_recovered,
    "Recovered: 80+":   count_age_80_up_recovered,
    "Peak Infected": max_active_cases_counter,
    "Peak Date": max_active_cases_counter
}            
        

param_sweep_default_scenario = BatchRunner(GridSimulationEnvironment,
                          variable_parameters = variable_params, 
                          fixed_parameters = default_scenario_model_params,
                          iterations = 1, 
                          max_steps = 1,
                          model_reporters = model_reporters)

param_sweep_default_scenario.run_all()

param_sweep_default_scenario_df = param_sweep_default_scenario.get_model_vars_dataframe()
param_sweep_default_scenario_df.to_csv("param_sweep_default_scenario_df.csv")


param_sweep_default_vaccination_scenario = BatchRunner(GridSimulationEnvironment,
                          variable_parameters = variable_params, 
                          fixed_parameters = default_vaccination_model_params,
                          iterations = 1, 
                          max_steps = 1,
                          model_reporters = model_reporters)

param_sweep_default_vaccination_scenario.run_all()

param_sweep_default_vaccination_scenario_df = param_sweep_default_vaccination_scenario.get_model_vars_dataframe()
param_sweep_default_vaccination_scenario_df.to_csv("param_sweep_default_vaccination_scenario_df.csv")


param_sweep_mobility_vaccination_scenario = BatchRunner(GridSimulationEnvironment,
                          variable_parameters = variable_params, 
                          fixed_parameters = mobility_vaccination_model_params,
                          iterations = 1, 
                          max_steps = 1,
                          model_reporters = model_reporters)

param_sweep_mobility_vaccination_scenario.run_all()

param_sweep_mobility_vaccination_scenario_df = param_sweep_mobility_vaccination_scenario.get_model_vars_dataframe()
param_sweep_mobility_vaccination_scenario_df.to_csv("param_sweep_mobility_vaccination_scenario_df.csv")


param_sweep_elderly_vaccination_scenario = BatchRunner(GridSimulationEnvironment,
                          variable_parameters = variable_params, 
                          fixed_parameters = elderly_vaccination_model_params,
                          iterations = 1, 
                          max_steps = 1,
                          model_reporters = model_reporters)

param_sweep_elderly_vaccination_scenario.run_all()

param_sweep_elderly_vaccination_scenario_df = param_sweep_elderly_vaccination_scenario.get_model_vars_dataframe()
param_sweep_elderly_vaccination_scenario_df.to_csv("param_sweep_elderly_vaccination_scenario_df.csv")


param_sweep_all_configuration_vaccination_scenario = BatchRunner(GridSimulationEnvironment,
                          variable_parameters = variable_params, 
                          fixed_parameters = all_configuration_vaccination_model_params,
                          iterations = 1, 
                          max_steps = 1,
                          model_reporters = model_reporters)

param_sweep_all_configuration_vaccination_scenario.run_all()

param_sweep_all_configuration_vaccination_scenario_df = param_sweep_all_configuration_vaccination_scenario.get_model_vars_dataframe()
param_sweep_all_configuration_vaccination_scenario_df.to_csv("param_sweep_all_configuration_vaccination_scenario_df.csv")
