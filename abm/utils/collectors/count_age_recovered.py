from abm.models.enum.status import Status
from abm.utils.collectors.count_age_status import count_age_status
        
def count_age_0_9_recovered(model):
    count = count_age_status(model, 0, 9, Status.Recovered)
    return count

def count_age_10_19_recovered(model):
    count = count_age_status(model, 10, 19, Status.Recovered)
    return count

def count_age_20_29_recovered(model):
    count = count_age_status(model, 20, 29, Status.Recovered)
    return count

def count_age_30_39_recovered(model):
    count = count_age_status(model, 30, 39, Status.Recovered)
    return count

def count_age_40_49_recovered(model):
    count = count_age_status(model, 40, 49, Status.Recovered)
    return count

def count_age_50_59_recovered(model):
    count = count_age_status(model, 50, 59, Status.Recovered)
    return count

def count_age_60_69_recovered(model):
    count = count_age_status(model, 60, 69, Status.Recovered)
    return count

def count_age_70_79_recovered(model):
    count = count_age_status(model, 70, 79, Status.Recovered)
    return count

def count_age_80_up_recovered(model):
    count = count_age_status(model, 80, 100, Status.Recovered)
    return count
