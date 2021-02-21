### This code needs further clean up and refactor

import numpy as np
import pandas as pd 
import json

from abm.resources.util import DATA_DROP_CSV_FILE
from abm.resources.util import QUEZON_CITY_DATA, QUEZON_CITY_DATA_LOC
from abm.resources.util import extract_data_drop_file

from abm.utils.modules.epi_data_extractor import epi_data_extractor
from abm.utils.modules.age_group_extractor import case_fatality_age_group_values
from abm.utils.modules.optimization.vaccine_distribution_optimization import vaccine_distribution_optimization
from abm.utils.modules.json_updater import json_updater

pd.options.mode.chained_assignment = None

import os.path

if not os.path.isfile(DATA_DROP_CSV_FILE):
   extract_data_drop_file()

data = pd.read_csv(DATA_DROP_CSV_FILE, index_col = 0)

district_1_psgc = [137404001, 137404009, 137404012, 137404013, 137404018, 137404026, 137404027,
137404029, 137404042, 137404049, 137404054, 137404056, 137404058, 137404061,
137404064, 137404065, 137404069, 137404073, 137404076, 137404078, 137404081,
137404084, 137404089, 137404093, 137404094, 137404096, 137404099, 137404100,
137404104, 137404107, 137404118, 137404129, 137404130, 137404133]

district_2_psgc = [137404010, 137404022, 137404138, 137404139, 137404140]

district_3_psgc = [137404002, 137404007, 137404011, 137404014, 137404015, 137404016, 137404019,
137404021, 137404030, 137404034, 137404035, 137404036, 137404037, 137404038,
137404039, 137404040, 137404053, 137404055, 137404059, 137404062, 137404063,
137404066, 137404067, 137404077, 137404085, 137404086, 137404087, 137404088,
137404102, 137404114, 137404115, 137404117, 137404126, 137404131, 137404132,
137404134]

district_4_psgc = [137404006, 137404041, 137404043, 137404046, 137404068, 137404070, 137404079,
137404095, 137404097, 137404136, 137404141, 137404142]


district_5_psgc = [137404006, 137404041, 137404043, 137404046, 137404068, 137404070, 137404079,
137404095, 137404097, 137404136, 137404141, 137404142]


district_6_psgc = [137404003, 137404005, 137404023, 137404025, 137404080, 137404111, 137404119,
137404120, 137404127, 137404135, 137404137]

district_1_psgc = ["PH%i"%(psgc_code) for psgc_code in district_1_psgc]
district_2_psgc = ["PH%i"%(psgc_code) for psgc_code in district_2_psgc]
district_3_psgc = ["PH%i"%(psgc_code) for psgc_code in district_3_psgc]
district_4_psgc = ["PH%i"%(psgc_code) for psgc_code in district_4_psgc]
district_5_psgc = ["PH%i"%(psgc_code) for psgc_code in district_5_psgc]
district_6_psgc = ["PH%i"%(psgc_code) for psgc_code in district_6_psgc]

qc_districts = district_1_psgc + district_2_psgc + district_3_psgc + district_4_psgc + district_5_psgc + district_6_psgc
qc_district_psgc_codes = [district_1_psgc, district_2_psgc, district_3_psgc, district_4_psgc, district_5_psgc, district_6_psgc]

def preprocessed(data):
    cases_df = data[['Age','AgeGroup','Sex','DateResultRelease','DateRecover','DateDied', 'RegionRes', 'ProvRes', 'CityMunRes','BarangayPSGC', 'RemovalType']]
    cases_df['DateResultRelease'] = pd.to_datetime(cases_df['DateResultRelease'])
    cases_df['DateRecover']       = pd.to_datetime(cases_df['DateRecover'])
    cases_df['DateDied']          = pd.to_datetime(cases_df['DateDied'])
    return data


def setup_qc(data):
    cases_df = preprocessed(data)
    cases_df = cases_df[cases_df["BarangayPSGC"].isin(qc_districts)]
    
    case_fatality_age_group = case_fatality_age_group_values(cases_df)

    mortality_rates = QUEZON_CITY_DATA["MORTALITY_RATE"]
    
    for index, mortality_rate in enumerate(mortality_rates):
        mortality_rates[mortality_rate]['rate'] = case_fatality_age_group[index] 

    json_updater(QUEZON_CITY_DATA_LOC, "MORTALITY_RATE", mortality_rates)
    
    districts_population = QUEZON_CITY_DATA["DISTRICT_POPULATION"]
    districts_data       = QUEZON_CITY_DATA["DISTRICT_DATA"]
    
    total_population    = 0
    total_susceptible   = 0
    total_infected      = 0
    total_recovered     = 0
    total_dead          = 0
    
    susceptible_population_lists = []
    location_keys = []

    city_df             = epi_data_extractor(data,"CityMunRes","QUEZON CITY")
    total_infected      = city_df["Active Cases"][city_df.index[-1]] 
    total_recovered     = city_df["Reported Recovered"].sum() 
    total_dead          = city_df["Reported Died"].sum()
        
    for index, district_population in enumerate(districts_population):
        epidemic_df = epi_data_extractor(data,"BarangayPSGC",qc_district_psgc_codes[index])
        population = districts_population[district_population]["population"]
        susceptible_population_lists.append(population)
        location_keys.append(district_population)
                
        infected        = epidemic_df['Case Incidence'].sum() 
        recovered       = epidemic_df['Reported Recovered'].sum() 
        dead            = epidemic_df['Reported Died'].sum() 
        susceptible     = 1 - (infected + recovered + dead) / population
        
        total_population    += population
        
        districts_data[district_population]["susceptible"] = susceptible 
        districts_data[district_population]["infected"]    = infected / population
        districts_data[district_population]["recovered"]   = recovered / population
        districts_data[district_population]["dead"]        = dead / population
        
    total_susceptible     = 1 - (total_infected + total_recovered + total_dead) / total_population
            
    json_updater(QUEZON_CITY_DATA_LOC, "DISTRICT_DATA", districts_data)
    json_updater(QUEZON_CITY_DATA_LOC, "POPULATION", int(total_population/QUEZON_CITY_DATA["SCALE"]))
    json_updater(QUEZON_CITY_DATA_LOC, "INFECTED", total_infected/total_population)
    json_updater(QUEZON_CITY_DATA_LOC, "RECOVERED", total_recovered/total_population)
    json_updater(QUEZON_CITY_DATA_LOC, "DEAD", total_dead/total_population)
    json_updater(QUEZON_CITY_DATA_LOC, "SUSCEPTIBLE", total_susceptible)
    
    setup_vaccination_distribution()

def setup_vaccination_distribution():
    
    # Preprocessing Cases Information Data
     
    cases_df = preprocessed(data)
    cases_df = cases_df[cases_df["BarangayPSGC"].isin(qc_districts)]

    # Getting Population Data from json file

    age_distribution_percentages = []
    susceptible_population_lists = []
    location_keys = []    

    districts_population = QUEZON_CITY_DATA["DISTRICT_POPULATION"]
    
    for index, district_population in enumerate(districts_population):
        population = districts_population[district_population]["population"]
        susceptible_population_lists.append(population)
        location_keys.append(district_population)
    
    # Age Distribution from the Agents Environment
    
    population_distribution = QUEZON_CITY_DATA["POPULATION_DISTRIBUTION"]
    for index, population in enumerate(population_distribution):
        age_distribution_percentages.append(population_distribution[population]['value'] / QUEZON_CITY_DATA["POPULATION"])
        
    location_df = pd.DataFrame({"LOCATIONS": location_keys})
    location_df["Population"]   = susceptible_population_lists
    location_df["0 to 9"]       = 0.0000
    location_df["10 to 19"]     = 0.0000
    location_df["20 to 39"]     = 0.0000
    location_df["30 to 39"]     = 0.0000
    location_df["40 to 49"]     = 0.0000
    location_df["50 to 59"]     = 0.0000
    location_df["60 to 69"]     = 0.0000
    location_df["70 to 79"]     = 0.0000
    location_df["80+"]          = 0.0000
    
    susceptible_location_df = location_df.copy()
    
    # Populating the Cases Data - Age Stratified
    
    for index, row in location_df.iterrows():
        age_cases_df = cases_df[cases_df["BarangayPSGC"].isin(qc_district_psgc_codes[index])]
        age_cases_df = age_cases_df.dropna(subset=['Age','AgeGroup'])
        age_cases_df = age_cases_df['AgeGroup'].value_counts().rename_axis('Age Group').reset_index(name='Count')

        location_df.at[index,"0 to 9"] = age_cases_df[age_cases_df['Age Group']=="0 to 4"]["Count"].values + age_cases_df[age_cases_df['Age Group']=="5 to 9"]["Count"].values
        location_df.at[index,"10 to 19"] = age_cases_df[age_cases_df['Age Group']=="10 to 14"]["Count"].values + age_cases_df[age_cases_df['Age Group']=="15 to 19"]["Count"].values
        location_df.at[index,"20 to 39"] = age_cases_df[age_cases_df['Age Group']=="20 to 24"]["Count"].values + age_cases_df[age_cases_df['Age Group']=="25 to 29"]["Count"].values
        location_df.at[index,"30 to 39"] = age_cases_df[age_cases_df['Age Group']=="30 to 34"]["Count"].values + age_cases_df[age_cases_df['Age Group']=="35 to 39"]["Count"].values
        location_df.at[index,"40 to 49"] = age_cases_df[age_cases_df['Age Group']=="40 to 44"]["Count"].values + age_cases_df[age_cases_df['Age Group']=="45 to 49"]["Count"].values
        location_df.at[index,"50 to 59"] = age_cases_df[age_cases_df['Age Group']=="50 to 54"]["Count"].values + age_cases_df[age_cases_df['Age Group']=="55 to 59"]["Count"].values
        location_df.at[index,"60 to 69"] = age_cases_df[age_cases_df['Age Group']=="60 to 64"]["Count"].values + age_cases_df[age_cases_df['Age Group']=="65 to 69"]["Count"].values
        location_df.at[index,"70 to 79"] = age_cases_df[age_cases_df['Age Group']=="70 to 74"]["Count"].values + age_cases_df[age_cases_df['Age Group']=="75 to 79"]["Count"].values
        location_df.at[index,"80+"] = age_cases_df[age_cases_df['Age Group']=="80+"]["Count"].values

    # Populating the Susceptible Data - Age Stratified

    for index, row in susceptible_location_df.iterrows():

        susceptible_location_df.at[index,"0 to 9"] = row["Population"] * age_distribution_percentages[0]
        susceptible_location_df.at[index,"10 to 19"] = row["Population"] * age_distribution_percentages[1]
        susceptible_location_df.at[index,"20 to 39"] = row["Population"] * age_distribution_percentages[2]
        susceptible_location_df.at[index,"30 to 39"] = row["Population"] * age_distribution_percentages[3]
        susceptible_location_df.at[index,"40 to 49"] = row["Population"] * age_distribution_percentages[4]
        susceptible_location_df.at[index,"50 to 59"] = row["Population"] * age_distribution_percentages[5]
        susceptible_location_df.at[index,"60 to 69"] = row["Population"] * age_distribution_percentages[6]
        susceptible_location_df.at[index,"70 to 79"] = row["Population"] * age_distribution_percentages[7]
        susceptible_location_df.at[index,"80+"]      = row["Population"] * age_distribution_percentages[8]
    
    cases_population        = np.matrix(location_df.iloc[:,2:11].values).T
    susceptible_location    = np.matrix(susceptible_location_df.iloc[:,2:11].values).T
    
    available_vaccines = QUEZON_CITY_DATA["VACCINE_AVAILABLE"]
    vaccine_prioritization = QUEZON_CITY_DATA["VACCINE_PRIORITIZATION"]
    size = susceptible_location.shape

    # Start of Implementation for Vaccine Distribution Optimization

    sub_problems = []
    
    for index, prioritization in enumerate(vaccine_prioritization):
        if vaccine_prioritization[prioritization]["activated"] == 1:
            sub_problem  = np.empty(size[1], dtype=float)
            sub_problem.fill(vaccine_prioritization[prioritization]["value"])
            sub_problems.append(sub_problem)
                
    result = vaccine_distribution_optimization(susceptible_location,available_vaccines,  sub_problems = sub_problems)
    result_json = json.loads(result)
    
    # Since this agent based model doesn't implement location based, 
    # use optimal_allocation_per_age
    
    return result_json
        
def initialize_setup():
    setup_qc(data)
    
def recalculate_susceptibles():
    vaccine_distribution = QUEZON_CITY_DATA["VACCINE_DISTRIBUTION"]
    vaccination_distribution = setup_vaccination_distribution()
    for index, vaccine in enumerate(vaccine_distribution):
        vaccine_distribution[vaccine]["assign"] = vaccination_distribution[index]
    json_updater(QUEZON_CITY_DATA_LOC, "VACCINE_DISTRIBUTION", vaccine_distribution)    

def recalculate_susceptibles():
    vaccine_distribution = QUEZON_CITY_DATA["VACCINE_DISTRIBUTION"]
    vaccination_distribution = setup_vaccination_distribution()
    age_distribution = pd.DataFrame(vaccination_distribution["optimal_allocation_per_age"]).sum(axis=1).values
    for index, vaccine in enumerate(vaccine_distribution):
        vaccine_distribution[vaccine]["assign"] = age_distribution[index]
    json_updater(QUEZON_CITY_DATA_LOC, "VACCINE_DISTRIBUTION", vaccine_distribution)
                
    vaccination_location_distribution = QUEZON_CITY_DATA["VACCINE_DISTRIBUTION_LOCATION"]
    vaccine_location_distribution = []

    location_distribution = pd.DataFrame(vaccination_distribution["optimal_allocation_per_age"])
    location_distribution.index = ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80+"]

    for i, column in enumerate(location_distribution, start = 1):
        location_distribution_obj = {}
        location_distribution_obj["LOCATION"] = i
        location_distribution_obj["ALLOCATION"] = {}
        for j, row in enumerate(location_distribution[column]):
            key = location_distribution.index[j]
            location_distribution_obj["ALLOCATION"][key] = row
            
        vaccine_location_distribution.append(location_distribution_obj)
        
    vaccination_location_distribution["LOCATIONS"] = vaccine_location_distribution

    json_updater(QUEZON_CITY_DATA_LOC, "VACCINE_DISTRIBUTION_LOCATION", vaccination_location_distribution)
    

def recalculate_population(model):
    population_distribution = QUEZON_CITY_DATA["POPULATION_DISTRIBUTION"]
    for index, population in enumerate(population_distribution):
        agents  = model.get_susceptibles(population_distribution[population]['min'], population_distribution[population]['max'])
        value = 0
        for agent in agents:
            value += 1
        population_distribution[population]['value'] = value
    json_updater(QUEZON_CITY_DATA_LOC, "POPULATION_DISTRIBUTION", population_distribution)
