import os

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from simulation.grid.model import GridSimulationEnvironment
from abm.visualizations.portrayal import *
from abm.visualizations.inputs.sliders import *
from abm.visualizations.inputs.options import *
from abm.visualizations.inputs.checkboxes import *

from abm.visualizations.charts.summary import SummaryChartModule

from abm.visualizations.elements.total_cases import TotalCases
from abm.visualizations.elements.active_cases import ActiveCases
from abm.visualizations.elements.recovered import Recovered
from abm.visualizations.elements.summary import Summary

PORT = os.environ.get('PORT', '8524')
                
canvas_element = CanvasGrid(agent_portrayal, 60, 60, 900, 900)
summary_chart  = SummaryChartModule(900,420)
infected_chart  = SummaryChartModule(900, 420, data_collector='infected_agents',
            series = [
                {"Label": "Infected","Color": "Red"},
            ])

total_cases_element     = TotalCases()
active_cases_element    = ActiveCases()
recovered_element       = Recovered()
summary_element         = Summary()

## """
## Note that these following params should be adjusted relatively to scale used
## """

model_params = {
    "scale":                        1000,
    "height":                       60,
    "width":                        60,
    "model_desc":                   UserSettableParameter('static_text', value = "Model Parameters"),
    "scenarios":                    scenarios,
    "vaccination_implementation":   vaccination_implementation,   
    "vaccine_prior_lbl":            UserSettableParameter('static_text', value = "Vaccine Prioritization"),
    "health_workers":               health_workers_option,
    "public_admin":                 public_admin_option,
    "persons_with_difficulty":      gainful_workers_option,
    "gainful_workers":              persons_with_difficulty_option,
    "mobile_workforce":             mobile_workforce_option,
    "elderly":                      elderly_option,
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
}

components = [
    total_cases_element, 
    active_cases_element, 
    recovered_element, 
    canvas_element,  
    summary_element,
    summary_chart,
    infected_chart
]

server = ModularServer(
    GridSimulationEnvironment, components, "COVID19 Agent Based Model with Multi-Objective Optimization for Vaccine Distribution", model_params
)

server.port = PORT


