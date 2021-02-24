from mesa.visualization.UserParam import UserSettableParameter

health_workers_option               = UserSettableParameter('checkbox', 'Health Workers', value = True)
public_admin_option                 = UserSettableParameter('checkbox', 'Public Administration and Defense', value = True)
gainful_workers_option              = UserSettableParameter('checkbox', 'Gainful Workers by Occupational Group', value = True)
persons_with_difficulty_option      = UserSettableParameter('checkbox', 'Persons with Functional Difficulty', value = True)

mobile_workforce_option             = UserSettableParameter('checkbox', 'Mobile Workforce', value = True)
elderly_option                      = UserSettableParameter('checkbox', 'Elderly Population', value = True)


person_health_social_work_option = UserSettableParameter('checkbox', 'Persons with Human Health and Social Work Activities', value = True)
person_prof_tech_option          = UserSettableParameter('checkbox', 'Persons with Professional, Scientific and Technical Activities', value = True)
person_admin_support_option      = UserSettableParameter('checkbox', 'Persons with Administrative and Support Service Activities', value = True)
person_agriculture_option        = UserSettableParameter('checkbox', 'Persons under Agriculture, Forestry and Fishing Industry', value = True)
person_education_option          = UserSettableParameter('checkbox', 'Persons under Education Sectors', value = True)

social_household_4ps_active_option      = UserSettableParameter('checkbox', 'Number of Household Members of Active 4Ps', value = True)
social_bayanihan_grant_option           = UserSettableParameter('checkbox', 'Bayanihan Grant Allocations', value = True)

economics_tourists_option               = UserSettableParameter('checkbox', 'Tourist Arrivals', value = True)
economics_marine_fisheries_option       = UserSettableParameter('checkbox', 'Marine Municipality Fisheries Production', value = True)
economics_volume_fisheries_option       = UserSettableParameter('checkbox', 'Volume of Fisheries Production', value = True)
economics_livestock_inventory_option    = UserSettableParameter('checkbox', 'Livestock Inventory', value = True)
economics_volume_corn_option            = UserSettableParameter('checkbox', 'Volume of Corn Production', value = True)


vaccinate_young_option                  = UserSettableParameter('checkbox', 'Allow Vaccination for Ages 0-9?', value = False)
