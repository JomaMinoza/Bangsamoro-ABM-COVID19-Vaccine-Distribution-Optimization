from mesa.visualization.UserParam import UserSettableParameter

vaccine_hesitancy       = UserSettableParameter("slider", "Vaccine Hesitancy", 0.00, 0.00, 1.0, 0.01)
incubation_period       = UserSettableParameter("slider", "Incubation Period (in days)", 7, 0.5, 14.0, 0.1)
recovery_period         = UserSettableParameter("slider", "Recovery Period (in days)", 14, 0.5, 30, 0.1)
transmission_rate       = UserSettableParameter("slider", "Transmission Rate", 0.21, 0.01, 1.0, 0.01)
mortality_rate          = UserSettableParameter("slider", "Mortality Rate", 0.01, 0.01, 1.0, 0.01)
viral_load_probability  = UserSettableParameter("slider", "High Viral Load Probability", 0.00, 0.00, 1.0, 0.01)
wearing_masks           = UserSettableParameter("slider", "People Wearing Masks", 0.53, 0.1, 1.0, 0.05)
social_distance_limit   = UserSettableParameter("slider", "Minimum Physical Distance", 0.75, 0.1, 1.0, 0.05)
natural_immunity        = UserSettableParameter("slider", "Natural Immunity", 0.18, 0.01, 1.0, 0.05)
exercise                = UserSettableParameter("slider", "Physically Fit", 0.33, 0.1, 1.0, 0.01)
preexisting_conditions  = UserSettableParameter("slider", "Persons with Pre-existing Medical Condition", 0.22, 0.1, 1.0, 0.01)
minority_restrictions   = UserSettableParameter("slider", "Maximum Minor Age Restrictions", 15, 0, 21, 1)
adult_restrictions      = UserSettableParameter("slider", "Minimum Adult Age Restrictions", 65, 40, 100, 1)

