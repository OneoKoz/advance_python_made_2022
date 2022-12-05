import random
import cProfile
import weakref

from memory_profiler import profile

from classes.owner import create_owner, change_owner
from classes.main_house import create_main_house, change_main_house
from classes.flat import create_flat, change_flat, change_flat_weakref

COUNT_ELEMENTS = 1_000_000
pr = cProfile.Profile()
pr.enable()

all_owner = create_owner(COUNT_ELEMENTS)
all_main_houses = create_main_house(COUNT_ELEMENTS)
all_flats = create_flat(COUNT_ELEMENTS, all_owner, all_main_houses)

change_owner(all_owner)
change_main_house(all_main_houses)
change_flat(all_flats)
change_flat_weakref(all_flats, all_main_houses, all_owner)

pr.disable()
pr.print_stats()
