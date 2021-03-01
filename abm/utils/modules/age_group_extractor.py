import pandas as pd
import numpy as np

def age_group_extractor(data):
    x   = data.AgeGroup.value_counts().sort_index()
    idx = np.array([0, 2, 3, 4, 5, 6, 7, 8, 9, 1, 10, 11, 12, 13, 14, 15, 16])
    
    df = pd.DataFrame({
        "total_count": x.values
    })
        
    df.index = idx
    df.sort_index(inplace=True)
    df.index = x.index[np.argsort(idx)]
    return df

def recovered_age_group_extractor(data):
    
    idx = np.array([0, 2, 3, 4, 5, 6, 7, 8, 9, 1, 10, 11, 12, 13, 14, 15, 16])
    
    recovered_cases_df = data[["AgeGroup","RemovalType"]]
    recovered_cases_df = recovered_cases_df[recovered_cases_df["RemovalType"] == "RECOVERED"]
    recovered_cases_df = recovered_cases_df.groupby(["AgeGroup","RemovalType"])["RemovalType"].count()
    recovered_cases_df.index = recovered_cases_df.index[np.argsort(idx)]

    return recovered_cases_df

def mortality_age_group_extractor(data):
    
    mortality_cases_df = data[["AgeGroup","RemovalType"]]
    mortality_cases_df = mortality_cases_df[mortality_cases_df["RemovalType"] == "DIED"]
    mortality_cases_df = mortality_cases_df.groupby(["AgeGroup","RemovalType"])["RemovalType"].count()
    
    return mortality_cases_df

def infected_age_group_distribution(data, population = 2761720):

    df = age_group_extractor(data)    
    return df / population

def infected_age_group_values(data):

    df = age_group_extractor(data)    
    return df.total_count.values


def infection_age_group_values(data):
    
    infected_df          = age_group_extractor(data)
    
    infected_age_group_values = []
    
    
    infected_cases   = np.append(infected_df.total_count.values,0)
        
    for x_index, x_row in enumerate(infected_cases):
        if x_index % 2 == 1:
            cases =  np.sum([
                infected_cases[x_index],
                infected_cases[x_index - 1]
            ])
                                        
            infected_age_group_values.append(cases)    
                                    
    return infected_age_group_values

def case_fatality_age_group_values(data):
    
    infected_df          = age_group_extractor(data)
    
    mortality_df         = infected_df * 0
    mortality_cases_df   = mortality_age_group_extractor(data)

    case_fatality_age_group_values = []
    
    for x_index, x_row in mortality_df.iterrows():
        for c_index, c_row in mortality_cases_df.iteritems():
            if c_index[0] == x_index:
                mortality_df.loc[x_index] = c_row
    
    infected_cases   = np.append(infected_df.total_count.values,0)
    mortality_cases  = np.append(mortality_df.total_count.values,0)
        
    for x_index, x_row in enumerate(mortality_cases):
        if x_index % 2 == 1:
            cases =  np.sum([
                infected_cases[x_index],
                infected_cases[x_index - 1]
            ])
                            
            died = np.sum([
                mortality_cases[x_index],
                mortality_cases[x_index - 1]
            ])
            rate = died / cases
            
            case_fatality_age_group_values.append(rate)    
                                    
    return case_fatality_age_group_values

def case_fatality_age_group_extractor(data):
    
    infected_df          = age_group_extractor(data)
    
    mortality_df         = infected_df * 0
    mortality_cases_df   = mortality_age_group_extractor(data)
    
    case_fatality_age_group_values = []
    
    for x_index, x_row in mortality_df.iterrows():
        for c_index, c_row in mortality_cases_df.iteritems():
            if c_index[0] == x_index:
                mortality_df.loc[x_index] = c_row
                
    infected_cases   = np.append(infected_df.total_count.values,0)
    mortality_cases  = np.append(mortality_df.total_count.values,0)
        
    for x_index, x_row in enumerate(mortality_cases):
        if x_index % 2 == 1:
            cases =  np.sum([
                infected_cases[x_index],
                infected_cases[x_index - 1]
            ])
                            
            died = np.sum([
                mortality_cases[x_index],
                mortality_cases[x_index - 1]
            ])
            rate = died / cases
            
            case_fatality_age_group_values.append(rate)    

    case_fatality_age_df = pd.DataFrame({
        "case_fatality_rates": case_fatality_age_group_values
    })
        
    case_fatality_age_df.index = ["0 - 9", "10 - 19", "20 - 29", "30 - 39", "40 - 49", "50 - 59", "60 - 69", "70 - 79", "80+"]
                                                    
    return case_fatality_age_df
