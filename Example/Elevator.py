import random
import time
import threading

AVAILABLE = 0
OCCUPIED = 1

DIRECTION_UP = 1
DIRECTION_DOWN = -1
DIRECTION_NEUTRAL = 0

GROUND_FLOOR = 0

MAX_LOAD = 20

class Elevator():
    def __init__(self, name):
        self._current_floor = GROUND_FLOOR
        self._status = AVAILABLE
        self._direction = DIRECTION_NEUTRAL
        self.__name = 'Elevator ' + str(name)
        self._load = 0

    def get_elevator_name(self):
        return self.__name

    def set_status(self, status):
        self._status = status

    def set_direction(self, direction):
        self._direction = direction

    def set_floor(self, floor):
        self._current_floor = floor

    def set_load(self, load):
        self._load = load

    def set_unload(self, load):
        if load > self._load:
            raise ValueError('More out than already in?')
        self._load = self._load - load

        if self._load == 0:
            self.set_status(AVAILABLE)
            self.set_direction(DIRECTION_NEUTRAL)

    def is_overload(self):
        return self._load > MAX_LOAD

    def is_available_for_pickup(self, floor):
        gap = self.get_gap_to_floor(floor)
        if gap > 0:
            target_direction = DIRECTION_UP
        elif gap < 0:
            target_direction = DIRECTION_DOWN
        else:
            target_direction = DIRECTION_NEUTRAL
        return gap, (self._status == AVAILABLE or target_direction == self._direction) and not self.is_overload()

    def get_gap_to_floor(self, floor):
        return floor - self._current_floor

    def go_to_floor(self, floor, load):
        gap = self.get_gap_to_floor(floor)
        if gap > 0:
            self.set_direction(DIRECTION_UP)
            self.set_status(OCCUPIED)
            self.set_load(load)
            for i in range(1, gap + 1):
                print('.')
                print('Current floor for {}: {}'.format(self.get_elevator_name(), self._current_floor))
                print('.')
                print('{} is reaching floor {}'.format(self.get_elevator_name(), self._current_floor + 1))
                print('.')
                self.set_floor(self._current_floor + 1)
                time.sleep(1)


class Elevator_Operator(object):
    def __init__(self, no_of_elevator):
        self.elv_list = self._create_elevators(no_of_elevator)
        self.thread_list = []

    def _create_elevators(self, no_of_elevator):
        elv_list = []
        for i in range(no_of_elevator):
            elv = Elevator(str(i))
            elv_list.append(elv)
        return elv_list

    def choose_elevator(self, floor):
        elv_dict = {}
        gap_list = []
        elv_tmp = []
        for elv in self.elv_list:
            gap, is_available = elv.is_available_for_pickup(floor)
            if is_available:
                gap_list.append(gap)
                elv_dict.update({elv: gap})

        min_gap = min(gap_list)
        for elv, gap in elv_dict.items():
            if gap == min_gap:
                elv_tmp.append(elv)

        return random.choice(elv_tmp)

    def call_elevator(self, info_dict):
        for key in info_dict.keys():
            floor = info_dict[key][0]
            load = info_dict[key][1]
            print('.')
            print('Calling for elevator to floor {} with {} passengers'.format(floor, load))
            print('.')
            chosen_elevator = self.choose_elevator(floor)
            if isinstance(chosen_elevator, Elevator):
                print('{} is chosen'.format(chosen_elevator.get_elevator_name()))
                tmp_thread = threading.Thread(target=chosen_elevator.go_to_floor, args=(floor, load))
                tmp_thread.start()
                self.thread_list.append(tmp_thread)

        for thread in self.thread_list:
            thread.join()

user_calls = {1: [5,5], 2: [8, 2], 3: [3,3]}
# user_calls = {1: [5,5]}
riverside = Elevator_Operator(2)
riverside.call_elevator(user_calls)
