from abm.models.enum.status import Status
from abm.models.enum.severity import Severity

from abm.utils.collectors.count_age_status import count_age_status
        
def count_age_0_9_infected(model):
    count = count_age_status(model, 0, 9, Status.Infected, severity =  Severity.Mild)
    return count

def count_age_10_19_infected(model):
    count = count_age_status(model, 10, 19, Status.Infected, severity =  Severity.Mild)
    return count

def count_age_20_29_infected(model):
    count = count_age_status(model, 20, 29, Status.Infected, severity =  Severity.Mild)
    return count

def count_age_30_39_infected(model):
    count = count_age_status(model, 30, 39, Status.Infected, severity =  Severity.Mild)
    return count

def count_age_40_49_infected(model):
    count = count_age_status(model, 40, 49, Status.Infected, severity =  Severity.Mild)
    return count

def count_age_50_59_infected(model):
    count = count_age_status(model, 50, 59, Status.Infected, severity =  Severity.Mild)
    return count

def count_age_60_69_infected(model):
    count = count_age_status(model, 60, 69, Status.Infected, severity =  Severity.Mild)
    return count

def count_age_70_79_infected(model):
    count = count_age_status(model, 70, 79, Status.Infected, severity =  Severity.Mild)
    return count

def count_age_80_up_infected(model):
    count = count_age_status(model, 80, 100, Status.Infected, severity =  Severity.Mild)
    return count
