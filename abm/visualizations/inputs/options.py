from mesa.visualization.UserParam import UserSettableParameter

scenarios                     = UserSettableParameter('choice', 'Scenarios', value='With Vaccination', choices=['No Vaccination', 'With Vaccination'])
vaccination_implementation    = UserSettableParameter('choice', 'Implementation', value='After 0 Days', choices=['After 0 Days', 'After 15 Days', 'After 30 Days', 'After 60 Days', 'After 120 Days'])