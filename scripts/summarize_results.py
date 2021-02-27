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

plt.style.use('ggplot')

plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['figure.dpi'] = 100

warnings.simplefilter('ignore')

titles = [
    "No Vaccination",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers - 25% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers - 50% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers - 75% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers - 100% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by Social Status",
    "Vaccine Distribution: Prioritization by Economic Impact and Revenue Generating Factors",
    "Vaccine Distribution: Prioritization Elderly",
    "Vaccine Distribution: Prioritization by All Factors",
    "Vaccine Distribution: Prioritization by All Factors - 25% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by All Factors - 50% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by All Factors - 75% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by All Factors - 100% Vaccine Hesitancy",
]

titles = [
    "No Vaccination",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers - 25% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers - 50% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers - 75% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by Frontliners and Essential Workers - 100% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by Social Status",
    "Vaccine Distribution: Prioritization by Economic Impact and Revenue Generating Factors",
    "Vaccine Distribution: Prioritization Elderly",
    "Vaccine Distribution: Prioritization by All Factors",
    "Vaccine Distribution: Prioritization by All Factors - 25% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by All Factors - 50% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by All Factors - 75% Vaccine Hesitancy",
    "Vaccine Distribution: Prioritization by All Factors - 100% Vaccine Hesitancy",
]


subtitles = [
    "Number of Exposed Agents",
    "Number of Infected Agents",
    "Number of Recovered Agents",
    "Number of Vaccinated Agents",
]

models = [
    "default_scenario_model",
    "default_vaccination_model",
    "default_vaccination_model_25_hesitancy",
    "default_vaccination_model_50_hesitancy",
    "default_vaccination_model_75_hesitancy",
    "default_vaccination_model_100_hesitancy",
    "mobility_vaccination_model",
    "elderly_vaccination_model",
    "social_vaccination_model",
    "all_configuration_vaccination_model",
    "all_configuration_vaccination_model_25_hesitancy",
    "all_configuration_vaccination_model_50_hesitancy",
    "all_configuration_vaccination_model_75_hesitancy",
    "all_configuration_vaccination_model_100_hesitancy",
]

collectors = [
    "agents_exposed",
    "agents_infected",
    "agents_recovered"
]


num_iterations = 20
num_steps      = 240


for model_idx, model in enumerate(models):
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
        summary_df.at[index,"Susceptible"]  = np.mean([data[i]["Susceptible"][index] for i in range(0,num_iterations)])
        summary_df.at[index,"Exposed"]      = np.mean([data[i]["Exposed"][index] for i in range(0,num_iterations)])
        summary_df.at[index,"Infected"]     = np.mean([data[i]["Infected"][index] for i in range(0,num_iterations)])
        summary_df.at[index,"Recovered"]    = np.mean([data[i]["Recovered"][index] for i in range(0,num_iterations)])
        summary_df.at[index,"Deaths"]       = np.mean([data[i]["Deaths"][index] for i in range(0,num_iterations)])
        summary_df.at[index,"Vaccinated"]   = np.mean([data[i]["Vaccinated"][index] for i in range(0,num_iterations)])
        
    summary_df.plot.line()    
    plt.title(titles[model_idx])
    plt.suptitle("Number of Agents per States", y = 0.05)
    plt.savefig("experiments/notebooks/summarized/{0}/{1}.png".format(model, "agents_summary"))    
    
    summary_df.to_csv("experiments/notebooks/summarized/{0}/agents_summary.csv".format(model))

    
    for collector_idx, collector in enumerate(collectors):
        collector_data = []
        
        for iter in range(0, num_iterations):
            df = pd.read_csv("experiments/notebooks/results/{0}/{1}/{2}.csv".format(model, collector, iter), index_col = 0)
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
            
        summary_df.plot.line(color=['b', 'g', 'r', 'c', 'm', 'y', 'k','gold', "orange"])   
        plt.title(titles[model_idx])
        plt.suptitle(subtitles[collector_idx], y = 0.05)
        plt.savefig("experiments/notebooks/summarized/{0}/{1}.png".format(model, collector))
        
        summary_df.to_csv("experiments/notebooks/summarized/{0}/{1}.csv".format(model, collector))


summarized_df = []
for model_idx, model in enumerate(models):
    summarized_df.append(pd.read_csv("experiments/notebooks/summarized/{0}/agents_summary.csv".format(model), index_col = 0))
    
labels = [
    "No Vaccination",
    "Prioritization by Frontliners and Essential Workers",
    "Prioritization by Frontliners and Essential Workers - 25% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 50% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 75% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 100% Vaccine Hesitancy",
    "Prioritization by Social Status",
    "Prioritization by Economic Impact",
    "Prioritization Elderly",
    "Prioritization by All Factors",    
    "Prioritization by All Factors - 25% Vaccine Hesitancy",
    "Prioritization by All Factors - 50% Vaccine Hesitancy",
    "Prioritization by All Factors - 75% Vaccine Hesitancy",
    "Prioritization by All Factors - 100% Vaccine Hesitancy",
]

                         
exposed_df      = pd.DataFrame({}, columns = labels)
infected_df     = pd.DataFrame({}, columns = labels)
recovered_df    = pd.DataFrame({}, columns = labels)
died_df         = pd.DataFrame({}, columns = labels)

for i in range(num_steps):
    for model_idx, model in enumerate(models):
        exposed_df.at[i,labels[model_idx]]        = summarized_df[model_idx].at[i,"Exposed"]
        infected_df.loc[i,labels[model_idx]]      = summarized_df[model_idx].at[i,"Infected"]
        recovered_df.loc[i,labels[model_idx]]     = summarized_df[model_idx].at[i,"Recovered"]
        died_df.loc[i,labels[model_idx]]          = summarized_df[model_idx].at[i,"Deaths"]
        
exposed_df.to_csv("experiments/notebooks/summarized/summary/exposed.csv")
infected_df.to_csv("experiments/notebooks/summarized/summary/infected.csv")
recovered_df.to_csv("experiments/notebooks/summarized/summary/recovered.csv")
died_df.to_csv("experiments/notebooks/summarized/summary/died.csv")


exposed_df[[
    "Prioritization by Frontliners and Essential Workers",
    "Prioritization by Social Status",
    "Prioritization by Economic Impact",
    "Prioritization Elderly",
    "Prioritization by All Factors",
]].plot.line()

plt.title("Vaccination Strategies: Number of Exposed Agents")
plt.savefig("experiments/notebooks/summarized/summary/vaccination_strategy-exposed-0.png")

infected_df[[
    "Prioritization by Frontliners and Essential Workers",
    "Prioritization by Social Status",
    "Prioritization by Economic Impact",
    "Prioritization Elderly",
    "Prioritization by All Factors",
]].plot.line()

plt.title("Vaccination Strategies: Number of Infected Agents")
plt.savefig("experiments/notebooks/summarized/summary/vaccination_strategy-infected-0.png")

recovered_df[[
    "Prioritization by Frontliners and Essential Workers",
    "Prioritization by Social Status",
    "Prioritization by Economic Impact",
    "Prioritization Elderly",
    "Prioritization by All Factors",
]].plot.line()

plt.title("Vaccination Strategies: Number of Recovered Agents")
plt.savefig("experiments/notebooks/summarized/summary/vaccination_strategy-recovered-0.png")

died_df[[
    "Prioritization by Frontliners and Essential Workers",
    "Prioritization by Social Status",
    "Prioritization by Economic Impact",
    "Prioritization Elderly",
    "Prioritization by All Factors",
]].plot.line()

plt.title("Vaccination Strategies: Number of Died Agents")
plt.savefig("experiments/notebooks/summarized/summary/vaccination_strategy-died-0.png")


exposed_df[[
    "No Vaccination",
    "Prioritization by Frontliners and Essential Workers",
    "Prioritization by Social Status",
    "Prioritization by Economic Impact",
    "Prioritization Elderly",
    "Prioritization by All Factors",
]].plot.line()

plt.title("Vaccination Strategies: Number of Exposed Agents")
plt.savefig("experiments/notebooks/summarized/summary/vaccination_strategy-exposed.png")

infected_df[[
    "No Vaccination",
    "Prioritization by Frontliners and Essential Workers",
    "Prioritization by Social Status",
    "Prioritization by Economic Impact",
    "Prioritization Elderly",
    "Prioritization by All Factors",
]].plot.line()

plt.title("Vaccination Strategies: Number of Infected Agents")
plt.savefig("experiments/notebooks/summarized/summary/vaccination_strategy-infected.png")

recovered_df[[
    "No Vaccination",
    "Prioritization by Frontliners and Essential Workers",
    "Prioritization by Social Status",
    "Prioritization by Economic Impact",
    "Prioritization Elderly",
    "Prioritization by All Factors",
]].plot.line()

plt.title("Vaccination Strategies: Number of Recovered Agents")
plt.savefig("experiments/notebooks/summarized/summary/vaccination_strategy-recovered.png")

died_df[[
    "No Vaccination",
    "Prioritization by Frontliners and Essential Workers",
    "Prioritization by Social Status",
    "Prioritization by Economic Impact",
    "Prioritization Elderly",
    "Prioritization by All Factors",
]].plot.line()

plt.title("Vaccination Strategies: Number of Died Agents")
plt.savefig("experiments/notebooks/summarized/summary/vaccination_strategy-died.png")

    
infected_hesitancy_df = infected_df[[
    "Prioritization by Frontliners and Essential Workers",
    "Prioritization by Frontliners and Essential Workers - 25% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 50% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 75% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 100% Vaccine Hesitancy",
]]

infected_hesitancy_df.columns = [
    "Prioritization by Frontliners and Essential Workers - 0% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 25% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 50% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 75% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 100% Vaccine Hesitancy",
]

infected_hesitancy_df.plot.line()

plt.title("Prioritization by Frontliners and Essential Workers: Number of Infected Agents")
plt.savefig("experiments/notebooks/summarized/summary/vaccination_strategy-frontliners-infected-hesitancy.png")

recovered_hesitancy_df = recovered_df[[
    "Prioritization by Frontliners and Essential Workers",
    "Prioritization by Frontliners and Essential Workers - 25% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 50% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 75% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 100% Vaccine Hesitancy",
]]

recovered_hesitancy_df.columns = [
    "Prioritization by Frontliners and Essential Workers - 0% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 25% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 50% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 75% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 100% Vaccine Hesitancy",
]

recovered_hesitancy_df.plot.line()

plt.title("Prioritization by Frontliners and Essential Workers: Number of Recovered Agents")
plt.savefig("experiments/notebooks/summarized/summary/vaccination_strategy-frontliners-recovered-hesitancy.png")

died_hesitancy_df = died_df[[
    "Prioritization by Frontliners and Essential Workers",
    "Prioritization by Frontliners and Essential Workers - 25% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 50% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 75% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 100% Vaccine Hesitancy",
]]

died_hesitancy_df.columns = [
    "Prioritization by Frontliners and Essential Workers - 0% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 25% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 50% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 75% Vaccine Hesitancy",
    "Prioritization by Frontliners and Essential Workers - 100% Vaccine Hesitancy",
]
died_hesitancy_df.plot.line()

plt.title("Prioritization by Frontliners and Essential Workers: Number of Died Agents")
plt.savefig("experiments/notebooks/summarized/summary/vaccination_strategy-frontliners-died-hesitancy.png")
