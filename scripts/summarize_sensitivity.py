import os
import sys

import warnings
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, os.getcwd() + '/../')
sys.path.insert(0, os.getcwd() + '/../abm/')
sys.path.insert(0, os.getcwd() + '/../simulation/')
sys.path.insert(0, os.getcwd() + '/../mesa/')
sys.path.insert(0, os.getcwd() + '/../experiments/')


def get_max_infections(model):
    df = pd.read_csv("experiments/notebooks/summarized/{0}/agents_summary.csv".format(model), index_col = 0)
    return np.max(df.loc[:,['Infected']])

def get_summarized_results(model):
    df = pd.read_csv("experiments/notebooks/summarized/{0}/agents_summary.csv".format(model), index_col = 0)
    df["Protection"] = df.loc[:,['Recovered','Vaccinated']].sum(axis = 1)
    return df

def get_summarized_prioritization_effects(model):
    df = get_summarized_results(model)
    df.drop(["Susceptible","Exposed","Infected"], axis = 1, inplace= True)
    return df.tail(1)

def get_summarized_deaths(model):
    df = get_summarized_results(model)
    df.drop(["Susceptible","Exposed","Infected","Recovered","Protection","Vaccinated"], axis = 1, inplace= True)
    return df.tail(1)

def get_summarized_protection(model):
    df = get_summarized_results(model)
    df.drop(["Susceptible","Exposed","Infected","Recovered","Deaths","Vaccinated"], axis = 1, inplace= True)
    return df.tail(1)


baseline_infection      = get_max_infections(model = "default_scenario_model")
baseline_deaths         = get_summarized_deaths(model = "default_scenario_model")

baseline_protection     = get_summarized_protection(model = "default_scenario_model")
baseline_vaccination    = get_summarized_prioritization_effects(model = "default_vaccination_model")

models = [
    "default_vaccination_model",
    "mobility_vaccination_model",
    "elderly_vaccination_model",
    "social_vaccination_model",
    "all_configuration_vaccination_model"
]

model_titles = [
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers, Social Status",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers, Economic Impact and Revenue Generating Factors",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers, Elderly",
    "Vaccine Distribution: Prioritization by All Factors",
]

default_vaccination_hesitancy_models = [
    "default_vaccination_model",
    "default_vaccination_model_25_hesitancy",
    "default_vaccination_model_50_hesitancy",
    "default_vaccination_model_75_hesitancy",
    "default_vaccination_model_100_hesitancy"
]

default_vaccination_hesitancy_model_titles = [
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers - 0% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers - 25% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers - 50% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers - 75% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers - 100% Vaccine Hesitancy",
]

print("\n-------------------------------------------------------------------------------------------------------\n")

print("---- Sensitivity Analysis on the Infected Agents ----")
print("Results showing percentage of infection reduction through different prioritization compared to no vaccination scenario\n")
for i, model in enumerate(models):
    results = get_max_infections(model = model)
    effect  = np.round((1 - (results.values / baseline_infection)) * 100, 3)
    print("{0} | {1}".format(model_titles[i], effect[0]))

print("\n-------------------------------------------------------------------------------------------------------\n")

print("---- Sensitivity Analysis on the Died Agents ----")
print("Results showing percentage of mortality reduction through different prioritization compared to no vaccination scenario\n")
for i, model in enumerate(models):
    results = get_summarized_deaths(model = model)
    effect  = np.round((1 - (results.values[0] / baseline_deaths.values[0]))*100, 3)
    print("{0} - {1}".format(model_titles[i], effect[0]))

print("\n-------------------------------------------------------------------------------------------------------\n")

print("---- Sensitivity Analysis on the Agents that were Protected ----")
print("Results showing percentage of protection* through different prioritization compared to no vaccination scenario\n")

for i, model in enumerate(models):
    results = get_summarized_protection(model = model)
    effect  = np.round(((results.values[0] / baseline_protection.values[0])*100), 3)
    print("{0} | {1}".format(model_titles[i], effect[0]))

print("\n-------------------------------------------------------------------------------------------------------\n")

print("---- Sensitivity Analysis on the Vaccine Hesitancy ----")

print("Results showing percentage of infection reduction through different prioritization compared to no vaccination scenario\n")
for i, model in enumerate(default_vaccination_hesitancy_models):
    results = get_max_infections(model = model)
    effect  = np.round((1 - (results.values / baseline_infection))*100, 3)
    print("{0} | {1}".format(default_vaccination_hesitancy_model_titles[i], effect[0]))

print("\n-------------------------------------------------------------------------------------------------------\n")

print("Results showing percentage of mortality reduction through different prioritization compared to no vaccination scenario\n")
for i, model in enumerate(default_vaccination_hesitancy_models):
    results = get_summarized_deaths(model = model)
    effect  = np.round((1 - (results.values[0] / baseline_deaths.values[0]))*100, 3)
    print("{0} | {1}".format(default_vaccination_hesitancy_model_titles[i], effect[0]))

print("\n-------------------------------------------------------------------------------------------------------\n")
    
print("Results showing percentage of protection* through different prioritization compared to no vaccination scenario\n")

for i, model in enumerate(default_vaccination_hesitancy_models):
    results = get_summarized_protection(model = model)
    effect  = np.round((results.values[0] / baseline_protection.values[0])*100, 3)
    print("{0} | {1}".format(default_vaccination_hesitancy_model_titles[i], effect[0]))

print("\n-------------------------------------------------------------------------------------------------------\n")

print("Note: * protection means making sure people to have immunity through vaccination and able to recovered")