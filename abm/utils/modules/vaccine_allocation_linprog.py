import numpy as np
import pandas as pd
import json

from scipy.optimize import linprog
from numpyencoder import NumpyEncoder

def vaccine_allocation_linprog(locations, doses, cases, age_population, mean_r0, available_vaccines):

    vaccine = np.empty(locations, dtype=int)
    obj_vaccine = np.empty(locations, dtype=int)

    vaccine.fill(doses)
    obj_vaccine.fill(1)

    vaccine = np.array([vaccine])

    susceptible = (age_population - cases)
    susceptible_population = susceptible.sum(axis=0)
    susceptible_percentage = susceptible/susceptible_population
    max_allowed_susceptible = susceptible.sum(axis=1)*(1-(mean_r0-1))
    available_vaccines = np.array([available_vaccines])

    lower_bound = np.empty(locations, dtype=int)
    lower_bound.fill(0)
    lower_bound

    vaccine_limit = list(map(lambda x, y:(x,y), lower_bound.tolist(),susceptible_population.tolist()[0]))
    
    opt = linprog(c=obj_vaccine, 
              A_ub=susceptible_percentage, 
              b_ub=max_allowed_susceptible, 
              A_eq=vaccine, 
              b_eq=available_vaccines, 
              bounds=vaccine_limit)

    return json.dumps({
        'susceptible_percentage': susceptible_percentage,
        'max_allowed_susceptible': max_allowed_susceptible,
        'available_vaccines': available_vaccines,
        'vaccine_limit': vaccine_limit,
        'optimal_allocation': opt.x,
        'optimal_allocation_per_age': susceptible_percentage * opt.x[0]
    },cls=NumpyEncoder)
    