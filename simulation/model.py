from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from abm.models.agents.person import Person

from abm.models.enum.status import Status
from abm.models.enum.viral_load import ViralLoad
from abm.models.enum.severity import Severity

from abm.resources.util import QUEZON_CITY_DATA, QUEZON_CITY_DATA_LOC
from abm.utils.modules.json_updater import json_updater

from abm.utils.collectors.total_susceptible import total_susceptible
from abm.utils.collectors.total_infected import total_infected
from abm.utils.collectors.total_deaths import total_deaths
from abm.utils.collectors.total_recovered import total_recovered
from abm.utils.collectors.total_vaccinated import total_vaccinated

from abm.utils.collectors import agents_information
from abm.utils.modules.setup import initialize_setup
from abm.utils.modules.setup import recalculate_susceptibles
from abm.utils.modules.setup import recalculate_population
from abm.utils.modules.setup import setup_vaccination_distribution

import numpy as np
            
class SimulationEnvironment(Model):
    description = (
        """
        An agent-based model that simulates COVID-19 transmission considering policy restrictions, behavioral and disease-resistance factors 
        as control measures to prevent further transmission of the virus. 
        
        Additionally, a multi-objective optimization for equitable vaccine distribution can be applied. 
        
        This considers the prioritization among health workers, public administration and defense, persons with difficulty, 
        gainful workers mobile workforce, and elderly population.
        """
    )
    
    def __init__(self, 
            height                  = 60, 
            width                   = 60, 
            incubation_period       = 7,
            recovery_period         = 1,
            transmission_rate       = 0.2,
            mortality_rate          = 0.1,
            viral_load_probability  = 0.7,
            wearing_masks           = 0.9,
            social_distance_limit   = 0.7,
            natural_immunity        = 0.2,
            exercise                = 0.4,
            preexisting_conditions  = 0.4,
            minority_restrictions   = 15,
            adult_restrictions      = 60,
            scenarios               = "No Vaccination",
            data                    = {},
            vaccination_implementation = 'No Vaccination',
            scale                   = 1000,
            health_workers          = True,
            public_admin            = True,
            persons_with_difficulty = True,
            gainful_workers         = True,
            mobile_workforce        = False,
            elderly                 = False
        ):
        
        ## Simulation Environment Setup
        
        self.height                             = height
        self.width                              = width
        self.scale                              = scale
        
        ## Simulation Environment Parameters
        
        self.scenarios                          = scenarios
        self.vaccination_implementation         = vaccination_implementation
        self.data                               = data
        self.incubation_period                  = incubation_period
        self.recovery_period                    = recovery_period
        self.transmission_rate                  = transmission_rate
        self.mortality_rate                     = mortality_rate
        self.viral_load_probability             = viral_load_probability

        ## Behavioral Factors

        self.wearing_masks                      = wearing_masks
        self.social_distance_limit              = social_distance_limit

        ## Disease-Resistance Factors

        self.natural_immunity                   = natural_immunity
        self.exercise                           = exercise
        self.preexisting_conditions             = preexisting_conditions
        self.immunity_threshold                 = natural_immunity * exercise * (1 - preexisting_conditions)
        
        # Policy Restrictions

        self.minority_restrictions              = minority_restrictions
        self.adult_restrictions                 = adult_restrictions
        
        ## Vaccine Prioritization
        
        self.health_workers                     = health_workers
        self.public_admin                       = public_admin
        self.persons_with_difficulty            = persons_with_difficulty
        self.gainful_workers                    = gainful_workers
        self.mobile_workforce                   = mobile_workforce
        self.elderly                            = elderly
        
        self.active_cases                       = 0
        self.total_cases                        = 0
        self.recovered                          = 0
                
        self.schedule                           = RandomActivation(self)
        self.grid                               = MultiGrid(width, height, torus=True)

        self.current_cycle                      = 0
        self.day                                = 0
        
        json_updater(QUEZON_CITY_DATA_LOC, "SCALE", self.scale)
        
        vaccine_prioritization = QUEZON_CITY_DATA["VACCINE_PRIORITIZATION"]
        
        vaccine_prioritization["frontliners_ratio"]["activated"]        = int(health_workers)
        vaccine_prioritization["public_admin"]["activated"]             = int(public_admin)
        vaccine_prioritization["persons_with_difficulty"]["activated"]  = int(persons_with_difficulty)
        vaccine_prioritization["gainful_workers"]["activated"]          = int(gainful_workers)
        vaccine_prioritization["mobile_workforce"]["activated"]         = int(mobile_workforce)
        vaccine_prioritization["elderly"]["activated"]                  = int(elderly)
        
        json_updater(QUEZON_CITY_DATA_LOC, "VACCINE_PRIORITIZATION", vaccine_prioritization)
        
        initialize_setup()
                
        self.data = QUEZON_CITY_DATA

        recalculate_susceptibles()
            
        self.datacollector = DataCollector(
            model_reporters = {
                "Susceptible": total_susceptible,
                "Infected": total_infected,
                "Deaths": total_deaths,
                "Recovered": total_recovered,
                "Vaccinated": total_vaccinated
            }
        )
        self.infected_agents = DataCollector(
            model_reporters = {
                "Infected": total_infected,
            }
        )
        
        self.initialized_all_agents()
        self.active_cases           = self.get_total_infected()
        self.total_cases            = self.get_total_cases()
        self.recovered              = self.get_total_recovered()
        recalculate_population(self)
        self.apply_vaccination_scheme()

        self.running = True
        self.datacollector.collect(self)
                                    
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.current_cycle      += 1
        self.day                += 1
        self.active_cases       =   self.get_total_infected()
        self.total_cases        =   self.get_total_infected() + self.get_total_recovered() + self.get_total_died()
        self.recovered          =   self.get_total_recovered()
        self.apply_vaccination_scheme()
        
    def get_total_susceptible(self):
        total = 0
        for agent in self.schedule.agents:
            if agent.is_susceptible():
                total += 1
        return total
    
    def get_total_vaccinated(self):
        total = 0
        for agent in self.schedule.agents:
            if agent.is_vaccinated():
                total += 1
        return total

    def get_total_infected(self):
        total = 0
        for agent in self.schedule.agents:
            if agent.is_infected():
                if agent.severity != Severity.Exposed:
                    total += 1
        return total

    def get_total_cases(self):
        total = 0
        for agent in self.schedule.agents:
            if (agent.is_infected() and (agent.severity != Severity.Exposed)) or agent.is_recovered() or agent.is_dead():
                total += 1
        return total

    def get_total_recovered(self):
        total = 0
        for agent in self.schedule.agents:
            if agent.is_recovered():
                total += 1
        return total

    def get_total_died(self):
        total = 0
        for agent in self.schedule.agents:
            if agent.is_dead():
                total += 1
        return total

    def roll_probability(self, threshold):
        return np.random.uniform(0.0, 1.0) < threshold

    def initialized_all_agents(self):

        population  = self.data["POPULATION"]
        susceptible = self.data["SUSCEPTIBLE"] * population
        infected    = self.data["INFECTED"]    * population
        exposed     = self.data["EXPOSED"]     * population        
        recovered   = self.data["RECOVERED"]   * population
        dead        = self.data["DEAD"]        * population
        
        self.initialized_agents(Status.Susceptible, susceptible)
        self.initialized_agents(Status.Infected, infected)
        self.initialized_agents(Status.Infected, exposed, severity_status = Severity.Exposed)        
        self.initialized_agents(Status.Recovered, recovered)
        self.initialized_agents(Status.Dead, dead)
            
    
    def initialized_agents(self, status, population, **kwargs):
    
        for i in range(int(population)):
            age         = np.random.beta(1.7,4.1)*100
            severity    = Severity.Zero
            viral_load  = ViralLoad.Zero
            facemask    = False
            immunity    = round(np.random.uniform(0,1),2)
            social_distancing = round(np.random.uniform(0,1),2)
            in_lockdown = False
            in_quarantine = False         
            
            severity_status = kwargs.get('severity_status', None)       
                        
            if status == Status.Infected:  
                if severity_status is None:
                    severity = Severity.Mild
                else:                    
                    severity = severity_status
                                        
                if self.roll_probability(self.viral_load_probability):
                    viral_load = ViralLoad.High
                else:
                    viral_load = ViralLoad.Low

            if self.roll_probability(self.wearing_masks):
                facemask   = True
                            
            if age > self.adult_restrictions:
                immunity = 1 - round(np.random.uniform(0,1) * self.preexisting_conditions, 2)
                if immunity < self.immunity_threshold:
                    in_lockdown = True
            
            if age < self.minority_restrictions:
                immunity = np.random.uniform(0,1) * self.natural_immunity
                in_lockdown = True
                
            agent = Person(self,
                    age = age,
                    facemask = facemask, 
                    social_distancing = social_distancing, 
                    immunity = immunity,
                    status = status,
                    viral_load = viral_load,
                    severity = severity,
                    in_quarantine = in_quarantine,
                    in_lockdown = in_lockdown)

            if agent.is_infected():
                agent.time_infected += 1
            
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))                
            self.schedule.add(agent)
            
    def get_vaccination_day(self):
        if self.vaccination_implementation == 'After 0 Days':
            return 0
        elif self.vaccination_implementation == 'After 15 Days':
            return 15
        elif self.vaccination_implementation == 'After 30 Days':
            return 30
        elif self.vaccination_implementation == 'After 60 Days':
            return 60
        elif self.vaccination_implementation == 'After 120 Days':
            return 120
        else:
            return 0
        
    def get_susceptibles(self, min_age, max_age):
        agents = []
        for agent in self.schedule.agents:
            if agent.is_susceptible():
                if (agent.age >= min_age) and (agent.age <= max_age):
                    agents.append(agent)
        return agents

    def get_agents(self, min_age, max_age):
        agents = []
        for agent in self.schedule.agents:
            if (agent.age >= min_age) and (agent.age <= max_age):
                agents.append(agent)
        return agents
        
    def inject_vaccine_doses(self, min_age, max_age, number_of_agents):
        agents = self.get_susceptibles(min_age, max_age)
        if len(agents) < number_of_agents:
            number_of_agents = len(agents)
            
        vaccinated_agents = self.random.sample(agents, k = number_of_agents)
        for agent in vaccinated_agents:
            agent.set_vaccinated()
        
    def apply_vaccination_scheme(self):
        if self.scenarios == 'With Vaccination':
            implementation_day = self.get_vaccination_day()
            if int(self.day) == implementation_day:
                recalculate_susceptibles()
                for distribution in self.data["VACCINE_DISTRIBUTION"]:
                    scheme = self.data["VACCINE_DISTRIBUTION"][distribution]
                    min_age = int(scheme['min'])
                    max_age = int(scheme['max'])
                    number_of_agents = int(scheme['assign'])
                    
                    self.inject_vaccine_doses(min_age, max_age, number_of_agents)
                    

                
            