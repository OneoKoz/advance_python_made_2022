import random

from memory_profiler import profile

from advance_05.custom_profile import profile_dec


class Owner:
    def __init__(self, name: str, age: int, marital_status: str, work: str):
        self.name = name
        self.age = age
        self.marital_status = marital_status
        self.work = work


@profile
@profile_dec
def create_owner(count: int):
    owner_name = ("Svetlana", "Ivan", "Gleb", "Petr", "Maria", "Anastasia")
    owner_age = (23, 34, 12, 43, 22, 63)
    owner_marr_status = ("married", "divorced", "single")
    owner_work = ("driver", "cook", "doctor", "lawyer", "programmer")

    owners = [None] * count
    for i in range(count):
        name = random.choice(owner_name)
        age = random.choice(owner_age)
        marr = random.choice(owner_marr_status)
        work = random.choice(owner_work)
        owners[i] = Owner(name, age, marr, work)
    return owners


@profile
@profile_dec
def change_owner(owners: list[Owner]):
    for i in range(len(owners)):
        owners[i].work = "NEW_WORK"
        owners[i].name = "NEW_NAME"
        owners[i].age += 10
        owners[i].marital_status = "NEW_STATUS"
