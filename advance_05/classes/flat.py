import random
import weakref

from memory_profiler import profile

from advance_05.custom_profile import profile_dec


class Flat:

    def __init__(self, number: int, entrance: int, num_room: int, main_house, owner):
        self.number = number
        self.entrance = entrance
        self.num_room = num_room

        self.main_house = weakref.ref(main_house)
        self.owner = weakref.ref(owner)


@profile
@profile_dec
def create_flat(count: int, owners, houses):
    flat_number = (1, 2, 3, 4, 45, 25)
    flat_entrance = (1, 2, 3, 4, 5, 7)
    flat_num_room = (1, 2, 3, 4)

    flats = [None] * count
    for i in range(count):
        number = random.choice(flat_number)
        entrance = random.choice(flat_entrance)
        num_room = random.choice(flat_num_room)

        owner = random.choice(owners)
        main_house = random.choice(houses)

        flats[i] = Flat(number, entrance, num_room, main_house, owner)
    return flats


@profile
@profile_dec
def change_flat(flats: list[Flat]):
    for val in flats:
        val.number += 10
        val.entrance += 10
        val.num_room += 10


@profile
@profile_dec
def change_flat_weakref(flats: list[Flat], houses: list, owner: list):
    for i, val in enumerate(flats):
        val.owner = weakref.ref(owner[i])
        val.main_house = weakref.ref(houses[i])
