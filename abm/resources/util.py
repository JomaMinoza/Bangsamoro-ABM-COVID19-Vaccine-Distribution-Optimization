import numpy as np
import json
import tarfile
import os

NUM_PROCS =  1
NUM_STEPS =  2
NUM_ITERATIONS =  1

PERSON_ICONS = {
  "SUSCEPTIBLE":  "abm/resources/img/happy.png",
  "EXPOSED":      "abm/resources/img/quiet.png",
  "INFECTED":     "abm/resources/img/confused.png",
  "RECOVERED":    "abm/resources/img/happy-1.png",
  "DIED":         "abm/resources/img/died.png",
  "ASYMPTOMATIC": "abm/resources/img/suspicious-1.png",
  "VACCINATED":   "abm/resources/img/in-love.png",
  "MILD":         "abm/resources/img/died.png",
  "CRITICAL":     "abm/resources/img/died.png",
  "VIRAL":        "abm/resources/img/ill.png",  
  "MASK":         "abm/resources/img/wearing-mask.png"
}

def get_current_path():    
    path = os.getcwd()
    if "notebooks" in path:
        path = os.path.abspath('../../') 
    return path

QUEZON_CITY_DATA_LOC = get_current_path() + "/abm/data/quezon_city.json"
QUEZON_CITY_DATA     = json.load(open(QUEZON_CITY_DATA_LOC))

BARMM_DATA_LOC = get_current_path() + "/abm/data/barmm.json"
BARMM_DATA     = json.load(open(BARMM_DATA_LOC))

NO_VACCINATION_SCENARIO_LOC      = get_current_path() + "/abm/data/params/no_vaccination_params.json"
NO_VACCINATION_SCENARIO_DATA     = json.load(open(NO_VACCINATION_SCENARIO_LOC))

VACCINATION_DAY0_SCENARIO_LOC       = get_current_path() + "/abm/data/params/vaccination_day0_params.json"
VACCINATION_DAY0_SCENARIO_DATA      = json.load(open(NO_VACCINATION_SCENARIO_LOC))


DATA_DROP_SRC           = get_current_path() + "/abm/data/sources/COVID-Data-12302020.csv.tar.gz"
DATA_DROP_CSV_FILE      = get_current_path()  + "/abm/data/sources/COVID-Data-12302020.csv"

def extract_data_drop_file():
    tar = tarfile.open(DATA_DROP_SRC, "r:gz")
    tar.extractall(path = get_current_path() + "/abm/data/sources/")
    tar.close()


def change_attribute(object, attribute, new_value):
    object.__dict__[attribute] = new_value
    return False

import numpy as np

def number_of_days(iteration):
    """
    Transform the iteration number in number of days
    :param iteration: int
    :return: number of days
    """
    return iteration // 24


def check_time(iteration, start, end):
    """
    Test if the iteration falls between a range of hours
    :param iteration:
    :param start: [0, 24]
    :param end: [0, 24]
    :return: boolean
    """
    return start <= iteration % 24 < end


def new_day(iteration):
    """
    :param iteration:
    :return:
    """
    return iteration % 24 == 0


def day_of_week(iteration):
    return (iteration // 24) % 7 + 1


def work_day(iteration):
    wd = day_of_week(iteration)
    return wd not in [1, 7]


def day_of_month(iteration):
    return (iteration // 24) % 30 + 1


def new_month(iteration):
    return day_of_month(iteration) == 1 and iteration % 24 == 0


def bed_time(iteration):
    return check_time(iteration,0,8)


def work_time(iteration):
    return check_time(iteration,8,16)


def lunch_time(iteration):
    return iteration % 24 == 12


def free_time(iteration):
    return check_time(iteration,17,24)


def sleep(a):
    if not new_day(a.iteration) and bed_time(a.iteration):
        return True
    return False


def reset(_list):
    _list = []


def sample_isolated(environment, isolation_rate, list_isolated):
    for a in environment.population:
        test = np.random.rand()
        if test <= isolation_rate:
            list_isolated.append(a.id)


def check_isolation(list_isolated, agent):
    if agent.id in list_isolated:
        agent.move_to_home()
        return True
    return False