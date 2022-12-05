import random
import weakref

from memory_profiler import profile


class Flat:

    def __init__(self, number: int, entrance: int, num_room: int, main_house, owner):
        self.number = number
        self.entrance = entrance
        self.num_room = num_room

        self.main_house = weakref.ref(main_house)
        self.owner = weakref.ref(owner)


@profile
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
def change_flat(flats: list[Flat]):
    for i in range(len(flats)):
        flats[i].number += 10
        flats[i].entrance += 10
        flats[i].num_room += 10


@profile
def change_flat_weakref(flats: list[Flat], houses: list, owner: list):
    for i in range(len(flats)):
        flats[i].owner = weakref.ref(owner[i])
        flats[i].main_house = weakref.ref(houses[i])
