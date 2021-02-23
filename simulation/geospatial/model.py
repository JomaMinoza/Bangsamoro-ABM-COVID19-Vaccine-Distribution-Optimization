# model.py
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from abm.models.agents.geospatial.person import Person

from abm.models.enum.status import Status
from abm.models.enum.viral_load import ViralLoad
from abm.models.enum.severity import Severity

from abm.utils.collectors.total_susceptible import total_susceptible
from abm.utils.collectors.total_exposed import total_exposed
from abm.utils.collectors.total_infected import total_infected
from abm.utils.collectors.total_deaths import total_deaths
from abm.utils.collectors.total_recovered import total_recovered
from abm.utils.collectors.total_vaccinated import total_vaccinated

from abm.utils.collectors.count_age_infected import *
from abm.utils.collectors.count_age_exposed import *
from abm.utils.collectors.count_age_died import *
from abm.utils.collectors.count_age_recovered import *
from abm.utils.collectors.count_age_vaccinated import *


from shapely.geometry import Point

import numpy as np

class GeoSimulationEnvironment(Model):
    
    description = (
        """
        An agent-based model that simulates COVID-19 transmission considering policy restrictions, behavioral and disease-resistance factors 
        as control measures to prevent further transmission of the virus. 
        
        Additionally, a multi-objective optimization for equitable vaccine distribution can be applied. 
        """
    )

    def __init__(
        self, 
        incubation_period       = 7,
        recovery_period         = 1,
        transmission_rate       = 0.2,
        viral_load_probability  = 0.0,
        wearing_masks           = 0.93,
        social_distance_limit   = 0.52,
        natural_immunity        = 0.2,
        exercise                = 0.4,
        preexisting_conditions  = 0.4,
        minority_restrictions   = 15,
        adult_restrictions      = 60,
        scenarios               = "No Vaccination",
        data                    = {},
        vaccination_implementation = 'After 0 Days',
        vaccine_hesitancy       = 0,
        health_workers          = False,
        public_admin            = False,
        persons_with_difficulty = False,
        gainful_workers         = False,
        mobile_workforce        = False,
        elderly                 = False,
        person_health_social_work = False,
        person_prof_tech          = False,
        person_admin_support      = False,
        person_education          = False,
        person_agriculture        = False,
        social_household_4ps_active     = False,
        social_bayanihan_grant          = False,
        economics_tourists              = False,
        economics_marine_fisheries      = False,
        economics_volume_fisheries      = False,
        economics_livestock_inventory   = False,
        economics_volume_corn           = False,
        environment             = object
        ):

        ## Simulation Environment Parameters
        
        self.scenarios                          = scenarios
        self.vaccination_implementation         = vaccination_implementation
        self.vaccine_hesitancy                  = vaccine_hesitancy
        
        self.data                               = data
        self.incubation_period                  = incubation_period
        self.recovery_period                    = recovery_period
        self.transmission_rate                  = transmission_rate
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
        
        self.person_health_social_work = person_health_social_work
        self.person_prof_tech          = person_prof_tech
        self.person_admin_support      = person_admin_support
        self.person_education          = person_education
        self.person_agriculture        = person_agriculture
        
        self.social_household_4ps_active     = social_household_4ps_active
        self.social_bayanihan_grant          = social_bayanihan_grant
        self.economics_tourists              = economics_tourists
        self.economics_marine_fisheries      = economics_marine_fisheries
        self.economics_volume_fisheries      = economics_volume_fisheries
        self.economics_livestock_inventory   = economics_livestock_inventory
        self.economics_volume_corn           = economics_volume_corn
        
        
        self.vaccine_prioritizations = {
            "person_health_social_work":        self.person_health_social_work,
            "person_prof_tech":                 self.person_prof_tech,
            "person_admin_support":             self.person_admin_support,
            "person_education":                 self.person_education,
            "person_agriculture":               self.person_agriculture,
            "elderly":                          self.elderly,
            "social_household_4ps_active":      self.social_household_4ps_active,
            "social_bayanihan_grant":           self.social_bayanihan_grant,
            "economics_tourists":               self.economics_tourists,
            "economics_marine_fisheries":       self.economics_marine_fisheries,
            "economics_volume_fisheries":       self.economics_volume_fisheries,
            "economics_livestock_inventory":    self.economics_livestock_inventory,
            "economics_volume_corn":            self.economics_volume_corn
        }


        self.active_cases                       = 0
        self.total_cases                        = 0
        self.recovered                          = 0
                
        self.schedule                           = RandomActivation(self)

        self.day                                = 0

        self.environment                        = environment
        self.grid                               = environment.get_geospace()

        self.schedule = RandomActivation(self)
        self.running = True
        
        self.localized_data_collectors          = environment.localized_data_collectors

        self.summary_data_collector = DataCollector(
            model_reporters = {
                "Susceptible": total_susceptible,
                "Exposed": total_exposed,                
                "Infected": total_infected,
                "Deaths": total_deaths,
                "Recovered": total_recovered,
                "Vaccinated": total_vaccinated
            }            
        )
        
        
        self.agents_infected_collector = DataCollector(
            model_reporters = {
                "0-9":   count_age_0_9_infected,
                "10-19": count_age_10_19_infected,
                "20-29": count_age_20_29_infected,
                "30-39": count_age_30_39_infected,
                "40-49": count_age_40_49_infected,
                "50-59": count_age_50_59_infected,
                "60-69": count_age_60_69_infected,
                "70-79": count_age_70_79_infected,
                "80+":   count_age_80_up_infected                
            }
        )
        
        self.agents_exposed_collector = DataCollector(
            model_reporters = {
                "0-9":   count_age_0_9_exposed,
                "10-19": count_age_10_19_exposed,
                "20-29": count_age_20_29_exposed,
                "30-39": count_age_30_39_exposed,
                "40-49": count_age_40_49_exposed,
                "50-59": count_age_50_59_exposed,
                "60-69": count_age_60_69_exposed,
                "70-79": count_age_70_79_exposed,
                "80+":   count_age_80_up_exposed                
            }
        )
        
        self.agents_died_collector = DataCollector(
            model_reporters = {
                "0-9":   count_age_0_9_died,
                "10-19": count_age_10_19_died,
                "20-29": count_age_20_29_died,
                "30-39": count_age_30_39_died,
                "40-49": count_age_40_49_died,
                "50-59": count_age_50_59_died,
                "60-69": count_age_60_69_died,
                "70-79": count_age_70_79_died,
                "80+":   count_age_80_up_died                
            }
        )

        self.agents_recovered_collector = DataCollector(
            model_reporters = {
                "0-9":   count_age_0_9_recovered,
                "10-19": count_age_10_19_recovered,
                "20-29": count_age_20_29_recovered,
                "30-39": count_age_30_39_recovered,
                "40-49": count_age_40_49_recovered,
                "50-59": count_age_50_59_recovered,
                "60-69": count_age_60_69_recovered,
                "70-79": count_age_70_79_recovered,
                "80+":   count_age_80_up_recovered                
            }
        )
        
        self.agents_vaccinated_collector = DataCollector(
            model_reporters = {
                "0-9":   count_age_0_9_vaccinated,
                "10-19": count_age_10_19_vaccinated,
                "20-29": count_age_20_29_vaccinated,
                "30-39": count_age_30_39_vaccinated,
                "40-49": count_age_40_49_vaccinated,
                "50-59": count_age_50_59_vaccinated,
                "60-69": count_age_60_69_vaccinated,
                "70-79": count_age_70_79_vaccinated,
                "80+":   count_age_80_up_vaccinated                
            }
        )
        
        self.initialized_all_agents()
        self.apply_vaccination_scheme()     
        
        
        self.update_data()
            
        
    def initialized_all_agents(self):
        for shape_idx, location_data in enumerate(self.environment.data, start = 1):
            population  = location_data["POPULATION"]
            susceptible = location_data["DATA"]["susceptible"] * population / self.environment.scale
            infected    = location_data["DATA"]["infected"]    * population / self.environment.scale
            recovered   = location_data["DATA"]["recovered"]   * population / self.environment.scale
            dead        = location_data["DATA"]["dead"]        * population / self.environment.scale
                                    
            self.initialized_agents(shape_idx, Status.Susceptible, susceptible)
            self.initialized_agents(shape_idx, Status.Infected, infected)
            self.initialized_agents(shape_idx, Status.Recovered, recovered)
            self.initialized_agents(shape_idx, Status.Dead, dead)
            print(location_data["LOCATION_NAME"], susceptible, infected, recovered, dead)

        return True

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
            
    def initialized_agents(self, shape_idx, status, population, **kwargs):
        
        location = "loc_" + str(shape_idx)
        
        hesitancy = [True, False]
        
        
        for i in range(int(np.ceil(population))):            
            pos_x, pos_y = self.grid.random_position(location)
            age         = np.random.beta(3.3, 6.1)*100
            severity    = Severity.Zero
            viral_load  = ViralLoad.Zero
            facemask    = False
            immunity    = round(self.random.normalvariate(self.immunity_threshold), 0.25 * self.immunity_threshold)
            social_distancing = round(self.random.normalvariate(self.self.social_distance_limit),0.25 * self.social_distance_limit) 
            in_lockdown = False
            in_quarantine = False         
            vaccine_hesistancy  = bool(np.random.choice(hesitancy, p = [self.vaccine_hesitancy, (1 - self.vaccine_hesitancy)]))
            
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
                adult_immunity  = round(self.random.normalvariate(self.preexisting_conditions),0.25 * self.preexisting_conditions)
                immunity = self.natural_immunity * self.exercise * (1 - adult_immunity)
                if immunity < self.immunity_threshold:
                    in_lockdown = True
            
            if age < self.minority_restrictions:
                young_immunity  = round(self.random.normalvariate(self.natural_immunity), 0.25 * self.natural_immunity)
                immunity = young_immunity * self.exercise * (1 - self.preexisting_conditions)                
                in_lockdown = True
                
            agent = Person(
                model               = self,
                shape               = Point(pos_x, pos_y),
                location            = location,
                age                 = age,
                facemask            = facemask, 
                social_distancing   = social_distancing, 
                immunity            = immunity,
                status              = status,
                viral_load          = viral_load,
                severity            = severity,
                in_quarantine       = in_quarantine,
                in_lockdown         = in_lockdown,
                vaccine_hesitant    = vaccine_hesistancy
            )

            if agent.is_infected():
                agent.time_infected += 1

            self.grid.add_agents(agent)
            self.schedule.add(agent)     

    def roll_probability(self, threshold):
        return np.random.uniform(0.0, 1.0) < threshold
    
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
        
    def recalculate_susceptibles(self):
        for idx, location_data in enumerate(self.environment.data):
            susceptible_agents = location_data["SUSCEPTIBLE_AGENTS"]
            location    = "loc_" + str(idx + 1)
            for susceptible_agent in susceptible_agents:
                min = susceptible_agents[susceptible_agent]["min"]
                max = susceptible_agents[susceptible_agent]["max"]
                value = len(self.get_localized_susceptibles(location, min, max))
                susceptible_agents[susceptible_agent]["value"] = value
                
            self.environment.recalculate_susceptible_agents(idx, susceptible_agents)

        self.environment.update_data()
                
    def get_susceptibles(self, min_age, max_age):
        agents = []
        for agent in self.schedule.agents:
            if agent.is_susceptible():
                if (min_age <= agent.age) and (agent.age <= max_age):
                    agents.append(agent)
        return agents

    def get_localized_agents(self, location):
        agents = []
        for agent in self.schedule.agents:
            if agent.location == location:
                agents.append(agent)
        return agents


    def get_localized_susceptibles(self, loc, min_age, max_age):
        agents = []
        for agent in self.get_susceptibles(min_age, max_age):
            if agent.location == loc:
                agents.append(agent)
        return agents

    def get_agents(self, min_age, max_age):
        agents = []
        for agent in self.schedule.agents:
            if (min_age <= agent.age) and (agent.age <= max_age):
                agents.append(agent)
        return agents

    def apply_vaccination_scheme(self):
        if self.scenarios == 'With Vaccination':
            implementation_day = self.get_vaccination_day()
            if int(self.day) == implementation_day:
                self.recalculate_susceptibles()   
                self.environment.initialize_sub_problems(self.vaccine_prioritizations)
                self.environment.update_vaccine_allocation()   

                for idx, location_data in enumerate(self.environment.data, start = 1):
                    location    = "loc_" + str(idx)
                    allocations = location_data["VACCINE_ALLOCATION"]
                    for allocation in allocations:
                        min_age             = allocations[allocation]["min"]
                        max_age             = allocations[allocation]["max"]
                        number_of_agents    = allocations[allocation]["value"]
                                        
                        self.inject_vaccine_doses(location, min_age, max_age, number_of_agents)
        
    def inject_vaccine_doses(self, location, min_age, max_age, number_of_agents):
        agents = self.get_localized_susceptibles(location, min_age, max_age)
        if len(agents) < number_of_agents:
            number_of_agents = len(agents)
        
        vaccinated_agents = self.random.sample(agents, k = int(number_of_agents))
        for agent in vaccinated_agents:
            agent.set_vaccinated()
    
    def update_data(self):
        for localized_data_collector in self.localized_data_collectors:
            localized_data_collector.collect(self)
            
        self.summary_data_collector.collect(self)
        self.agents_exposed_collector.collect(self)
        self.agents_infected_collector.collect(self)
        self.agents_died_collector.collect(self)
        self.agents_recovered_collector.collect(self)
        self.agents_vaccinated_collector.collect(self)

        
        self.active_cases       =   self.get_total_infected()
        self.total_cases        =   self.get_total_infected() + self.get_total_recovered() + self.get_total_died()
        self.recovered          =   self.get_total_recovered()

    def step(self):
        self.day += 1
        self.apply_vaccination_scheme()
        self.update_data()
        self.schedule.step()

        self.grid._recreate_rtree()





