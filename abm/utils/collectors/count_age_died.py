from abm.models.enum.status import Status
from abm.utils.collectors.count_age_status import count_age_status
        
def count_age_0_9_died(model):
    count = count_age_status(model, 0, 9, Status.Dead)
    return count

def count_age_10_19_died(model):
    count = count_age_status(model, 10, 19, Status.Dead)
    return count

def count_age_20_29_died(model):
    count = count_age_status(model, 20, 29, Status.Dead)
    return count

def count_age_30_39_died(model):
    count = count_age_status(model, 30, 39, Status.Dead)
    return count

def count_age_40_49_died(model):
    count = count_age_status(model, 40, 49, Status.Dead)
    return count

def count_age_50_59_died(model):
    count = count_age_status(model, 50, 59, Status.Dead)
    return count

def count_age_60_69_died(model):
    count = count_age_status(model, 60, 69, Status.Dead)
    return count

def count_age_70_79_died(model):
    count = count_age_status(model, 70, 79, Status.Dead)
    return count

def count_age_80_up_died(model):
    count = count_age_status(model, 80, 100, Status.Dead)
    return count
