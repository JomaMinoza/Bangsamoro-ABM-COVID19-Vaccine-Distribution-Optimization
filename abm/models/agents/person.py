from mesa import Agent

import numpy as np
import uuid

from abm.models.enum.agent_type import AgentType
from abm.models.enum.work_type import WorkType

from abm.models.enum.status import Status
from abm.models.enum.age_group import AgeGroup
from abm.models.enum.viral_load import ViralLoad
from abm.models.enum.severity import Severity

from abm.resources.util import QUEZON_CITY_DATA

class Person(Agent):
    def __init__(self, 
                    model, 
                    age = 25.7,
                    facemask = False, 
                    social_distancing = 0, 
                    immunity = 0,
                    status = Status.Susceptible,
                    viral_load = ViralLoad.Zero,
                    severity = Severity.Zero,
                    in_quarantine = False,
                    in_lockdown = False,
                    vaccine_hesitant = False
                  ):
        super().__init__(uuid.uuid4().hex, model)
        self.unique_id      = uuid.uuid4().hex
        self.model          = model
        self.age            = age
        self.age_group      = AgeGroup.A00to09
        self.facemask       = facemask
        self.distance       = round(social_distancing,2)
        self.immunity       = round(immunity,2)
        self.status         = status
        self.viral_load     = viral_load
        self.severity       = severity
        self.in_quarantine  = in_quarantine
        self.in_lockdown    = in_lockdown
        self.time_infected  = 0
        self.infection_rate = 0.00000
        self.mortality_rate = 0.00000
        self.vaccine_hesitant = vaccine_hesitant
        
        ## Economic Impacts - Work in Progress
        self.savings        = 0
        self.employed       = False
        self.work_type      = WorkType.Household
        
        
        self.set_age_group()
        self.set_mortality_rate()

    def get_description(self):
        if self.status == Status.Infected:
            return "{}({}) - Viral Load ({})".format(self.status.name, self.severity.name, self.viral_load.name)
        else:
            return self.status.name
          
    def set_age_group(self):
      if (self.age >= 0) and (self.age <= 9):
        self.age_group = AgeGroup.A00to09
      elif (self.age >= 10) and (self.age <= 19):
        self.age_group = AgeGroup.A10to19
      elif (self.age >= 20) and (self.age <= 29):
        self.age_group = AgeGroup.A20to29
      elif (self.age >= 30) and (self.age <= 39):
        self.age_group = AgeGroup.A30to39
      elif (self.age >= 40) and (self.age <= 49):
        self.age_group = AgeGroup.A40to49
      elif (self.age >= 50) and (self.age <= 59):
        self.age_group = AgeGroup.A50to59
      elif (self.age >= 60) and (self.age <= 69):
        self.age_group = AgeGroup.A50to59
      elif (self.age >= 70) and (self.age <= 79):
        self.age_group = AgeGroup.A70to79
      elif (self.age >= 80):
        self.age_group = AgeGroup.A80toXX

    def get_information(self):
      return {
        "unique_id":      self.unique_id,
        "status":         self.status.name,
        "severity":       self.severity.name,
        "facemask":       self.facemask,
        "viral_load":     self.viral_load,
        "time_infected":  self.time_infected,
        "age":            self.age
      }

    def __str__(self):
        return str(self.status.name)

    def get_status(self):
      return self.status
    
    def is_susceptible(self):
      return self.get_status() == Status.Susceptible

    def is_infected(self):
      return self.get_status() == Status.Infected

    def is_recovered(self):
      return self.get_status() == Status.Recovered

    def is_vaccinated(self):
      return self.get_status() == Status.Vaccinated

    def is_dead(self):
      return self.get_status() == Status.Dead

    def wearing_face_masks(self):
      return self.facemask

    def practicing_social_distancing(self):
      return self.distance > self.model.social_distance_limit

    def with_high_viral_load(self):
      return self.viral_load == ViralLoad.High

    def with_low_immunity(self):
      return self.immunity < self.model.immunity_threshold

    def roll_probability(self, threshold):      
      return np.random.uniform(0.0, 1.0) <= threshold

    def set_viral_load(self, load):
      if load == ViralLoad.High:
        self.viral_load = ViralLoad.Low
      else:
        if self.roll_probability(self.model.viral_load_probability):
            self.viral_load = ViralLoad.High
        else:
            self.viral_load = ViralLoad.Low
      
    def set_dead(self):
        self.status = Status.Dead

    def set_vaccinated(self):
      if not self.vaccine_hesitant:
        self.status = Status.Vaccinated
        self.viral_load = ViralLoad.Zero
        self.severity = Severity.Zero
        self.immunity = 0.9
        self.in_quarantine = False

    def set_recovered(self):
        self.status = Status.Recovered
        self.viral_load = ViralLoad.Zero
        self.severity = Severity.Zero
        self.immunity = 1
        self.in_quarantine = False

    def set_lockdown(self):
        self.in_lockdown = True

    def set_infected(self):
        if self.is_susceptible():
            self.status = Status.Infected
            self.severity = Severity.Exposed
            self.time_infected = 0
            
    def set_mortality_rate(self):
      mortality_rates = QUEZON_CITY_DATA["MORTALITY_RATE"]
      for mortality_rate in mortality_rates:
          agent_mortality_rate = mortality_rates[mortality_rate]
          min_age = int(agent_mortality_rate['min'])
          max_age = int(agent_mortality_rate['max'])
          if (min_age <= self.age) and (self.age <= max_age):
            self.mortality_rate = agent_mortality_rate['rate']
          
    def spread_virus(self):
        neighbors = self.model.grid.get_neighbors(
            pos = self.pos,
            moore = True,
            include_center = True)
        for neighbor in neighbors:
            if neighbor.is_susceptible() and not neighbor.in_lockdown:
              if self.with_high_viral_load() and neighbor.with_low_immunity():
                  neighbor.set_infected()
              else:
                if self.roll_probability(self.model.transmission_rate):
                  if (not neighbor.wearing_face_masks() or not neighbor.practicing_social_distancing()) and neighbor.with_low_immunity():
                      neighbor.set_infected()
                      neighbor.set_viral_load(self.viral_load)
                  

    def while_infected(self):
        self.time_infected += 1
        
        if self.severity == Severity.Exposed:
          if self.time_infected <= self.get_incubation_time():
            if self.with_low_immunity() and self.roll_probability((self.infection_rate)):
                self.in_quarantine = True
                self.severity = Severity.Mild
          else:
            self.status = Status.Susceptible
        else:
          if not self.in_quarantine:          
            self.spread_virus() 
          else:          
            if self.viral_load == ViralLoad.High:     
              if self.with_low_immunity():                
                if self.time_infected < self.model.incubation_period:
                    if self.roll_probability(self.model.transmission_rate):
                      self.in_quarantine = True                
                      self.severity = Severity.Mild
                else:
                  self.status = Status.Susceptible                
              else:
                self.status = Status.Susceptible
            else:
              if self.time_infected < self.model.incubation_period:
                if self.roll_probability(self.model.transmission_rate):
                  self.in_quarantine = True                
                  self.severity = Severity.Mild
              else:
                self.status = Status.Susceptible                
                          
        if self.time_infected < self.get_recovery_time():
            if self.roll_probability(self.mortality_rate):
                self.set_dead()
        else: 
            self.set_recovered()
            
    def get_recovery_time(self):
        return int(self.random.normalvariate(self.model.recovery_period, 7))

    def get_incubation_time(self):
        return int(self.random.normalvariate(self.model.incubation_period, 7))

    def move_to_next(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore = True,
            include_center = False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def move(self):
        if self.in_quarantine or self.in_lockdown or self.is_dead():
            pass
        else:
            self.model.grid.move_to_empty(self)
        if self.is_infected():
            self.while_infected()
            
        if self.is_susceptible() or not self.in_lockdown:
          if self.roll_probability(self.model.transmission_rate):
            if (not self.wearing_face_masks() or not self.practicing_social_distancing()) and self.with_low_immunity():
                self.set_infected()
                self.set_viral_load(self.viral_load)

    def step(self):
        if not self.is_dead():
            self.move()
