import numpy as np
import json

from scipy.optimize import linprog
from numpyencoder import NumpyEncoder


### Generates Matrix Constraints 
def matrix_constraints_generator(matrix_population, **kwargs):
    
    size = matrix_population.shape[0]
    sub_problems = kwargs.get('sub_problems', [])

    
    population             = matrix_population.sum(axis=0)
    
    ## population_percentage
    A_contraints           = matrix_population/population
    
    for index, sub_problem in enumerate(sub_problems):
        A_contraints = np.insert(A_contraints, size + index, sub_problem, axis=0)
        
    return (A_contraints, population)


### Generates Vector Constraints and Limit

def vector_constraints_generator(matrix_population, available_vaccines, **kwargs):
    
    size = matrix_population.shape[0]
    sub_problems = kwargs.get('sub_problems', [])
    
    population             = matrix_population.sum(axis=0)
    population_percentage  = matrix_population/population
    
    # max_allowed_susceptibles
    b_contraints           = matrix_population.sum(axis=1)
    
    available_vaccines = np.array([available_vaccines])

    lower_bound = np.empty(size, dtype=int)
    lower_bound.fill(0)
    
    # vaccine limit
    limit = list(map(lambda x, y:(x,y), lower_bound.tolist(), population.tolist()[0]))
    
    for index, sub_problem in enumerate(sub_problems):
        b_contraints = np.insert(b_contraints, size + index, available_vaccines, axis=0)
        
    return (b_contraints, limit)


# Main Optimization Scheme

def vaccine_distribution_optimization(matrix_population, available_vaccines, **kwargs):
    
    # dimension of the matrix constraints
    size = matrix_population.shape   
    
    sub_problems = kwargs.get('sub_problems', [])

    
    matrix_constraints, distribution = matrix_constraints_generator(matrix_population, **kwargs)
    vector_constraints, limit        = vector_constraints_generator(matrix_population, 
                                                                available_vaccines,
                                                                **kwargs)
    
    # Left Equality Constraints
    vaccine = np.empty(size[1], dtype=int)

    # Number of doses
    vaccine.fill(2)
    vaccine = np.array([vaccine])

    # Objective Function
    obj_vaccine = np.empty(size[1], dtype=int)
    obj_vaccine.fill(1)
    
    opt = linprog(
                c      = obj_vaccine, 
                A_ub   = matrix_constraints, 
                b_ub   = vector_constraints, 
                A_eq   = vaccine, 
                b_eq   = available_vaccines, 
                bounds = limit)

    return json.dumps({
        'susceptible_distribution':   distribution,
        'max_allowed_susceptibles':   matrix_population.sum(axis=1),
        'available_vaccines':         available_vaccines,
        'vaccine_limit':              limit,
        'optimal_allocation':         opt.x,
        'optimal_allocation_per_age': (matrix_population/matrix_population.sum(axis=0)) * opt.x[0]
    },cls=NumpyEncoder)
    