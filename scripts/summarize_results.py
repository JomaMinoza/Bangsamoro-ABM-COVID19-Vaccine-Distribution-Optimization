import os
import sys

import warnings
import numpy as np
import pandas as pd

sys.path.insert(0, os.getcwd() + '/../')
sys.path.insert(0, os.getcwd() + '/../abm/')
sys.path.insert(0, os.getcwd() + '/../simulation/')
sys.path.insert(0, os.getcwd() + '/../mesa/')
sys.path.insert(0, os.getcwd() + '/../experiments/')

warnings.simplefilter('ignore')

models = [
    "default_scenario_model",
    "default_vaccination_model",
    "default_vaccination_model_25_hesistancy",
    "default_vaccination_model_50_hesistancy",
    "default_vaccination_model_75_hesistancy",
    "default_vaccination_model_100_hesistancy",
    "mobility_vaccination_model",
    "elderly_vaccination_model",
    "social_vaccination_model",
    "all_configuration_vaccination_model",
    "all_configuration_vaccination_model_25_hesistancy",
    "all_configuration_vaccination_model_50_hesistancy",
    "all_configuration_vaccination_model_75_hesistancy",
    "all_configuration_vaccination_model_100_hesistancy",
]

num_iterations = 20

for i, model in enumerate(models):
    parent_dir = os.getcwd()
    scenario   = "experiments/notebooks/summarized/{0}".format(model)

    path = os.path.join(parent_dir, scenario) 
    os.makedirs(path,  exist_ok=True)
        
    data = []
    for i in range(0,num_iterations):
        df = pd.read_csv("experiments/notebooks/results/{0}/agents_summary/{1}.csv".format(model, i), index_col = 0)
        data.append(df)
        
    summary_df = data[0].copy()
    
    for index, row in summary_df.iterrows():
        summary_df.at[index,"Susceptible"] = np.mean([data[i]["Susceptible"][index] for i in range(0,10)])
        summary_df.at[index,"Infected"] = np.mean([data[i]["Infected"][index] for i in range(0,10)])
        summary_df.at[index,"Recovered"] = np.mean([data[i]["Recovered"][index] for i in range(0,10)])
        summary_df.at[index,"Deaths"] = np.mean([data[i]["Deaths"][index] for i in range(0,10)])
        summary_df.at[index,"Vaccinated"] = np.mean([data[i]["Vaccinated"][index] for i in range(0,10)])
        
        summary_df.to_csv("experiments/notebooks/summarized/{0}/agents_summary.csv".format(model, i))

    collectors = [
        "agents_exposed",
        "agents_infected",
        "agents_recovered",
        "agents_vaccinated",
    ]
    
    
    for collector in collectors:
        collector_data = []
        
        for i in range(0, num_iterations):
            df = pd.read_csv("experiments/notebooks/results/{0}/{1}/{2}.csv".format(model, collector, i), index_col = 0)
            collector_data.append(df)
            
        summary_df = collector_data[0].copy()

        for index, row in summary_df.iterrows():
            summary_df.at[index,"0-9"] = np.mean([collector_data[i]["0-9"][index] for i in range(0,num_iterations)])
            summary_df.at[index,"10-19"] = np.mean([collector_data[i]["10-19"][index] for i in range(0,num_iterations)])
            summary_df.at[index,"20-29"] = np.mean([collector_data[i]["20-29"][index] for i in range(0,num_iterations)])
            summary_df.at[index,"30-39"] = np.mean([collector_data[i]["30-39"][index] for i in range(0,num_iterations)])
            summary_df.at[index,"40-49"] = np.mean([collector_data[i]["40-49"][index] for i in range(0,num_iterations)])
            summary_df.at[index,"50-59"] = np.mean([collector_data[i]["50-59"][index] for i in range(0,num_iterations)])
            summary_df.at[index,"60-69"] = np.mean([collector_data[i]["60-69"][index] for i in range(0,num_iterations)])
            summary_df.at[index,"70-79"] = np.mean([collector_data[i]["70-79"][index] for i in range(0,num_iterations)])
            summary_df.at[index,"80+"]   = np.mean([collector_data[i]["80+"][index] for i in range(0,num_iterations)])
            
        summary_df.to_csv("experiments/notebooks/summarized/{0}/{1}.csv".format(model, collector))

