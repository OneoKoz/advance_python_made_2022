import random

from memory_profiler import profile

from advance_05.custom_profile import profile_dec, calculate_time


class MainHouse:
    __slots__ = ("num_house", "street", "num_free_flat", "num_residents", "city", '__weakref__')

    def __init__(self, num_house: int, street: str, num_free_flat: int,
                 num_residents: int, city: str = "Minsk"):
        self.num_house = num_house
        self.street = street
        self.num_free_flat = num_free_flat
        self.num_residents = num_residents
        self.city = city


@profile
@profile_dec
@calculate_time
def create_main_house(count: int):
    house_num_house = (100, 43, 11, 4, 50, 23)
    house_street = ("Main", "Broadway", "Park Avenue",
                    "St. Mark’s Place", "5th Avenue", "Washington Street")
    house_num_free_flat = (3, 20, 499)
    house_num_residents = (1111, 432, 4, 134, 243)

    houses = [None] * count
    for i in range(count):
        num_house = random.choice(house_num_house)
        street = random.choice(house_street)
        num_free_flat = random.choice(house_num_free_flat)
        num_residents = random.choice(house_num_residents)
        houses[i] = MainHouse(num_house, street, num_free_flat, num_residents)
    return houses


@profile
@profile_dec
@calculate_time
def change_main_house(houses: list[MainHouse]):
    for val in houses:
        val.num_house += 10
        val.city = "NEW CITY"
        val.street = "NEW STREET"
        val.num_free_flat += 10
        val.num_residents += 10
