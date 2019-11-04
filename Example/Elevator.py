import time

AVAILABLE = 0
OCCUPIED = 1

DIRECTION_UP = 1
DIRECTION_DOWN = -1
DIRECTION_NEUTRAL = 0

GROUND_FLOOR = 0

class Elevator(object):
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

    def is_available_for_pickup(self, floor):
        gap = self.get_gap_to_floor(floor)
        target_direction = DIRECTION_UP if gap > 0 else DIRECTION_DOWN
        return gap, (self._direction == DIRECTION_NEUTRAL or target_direction == self._direction)

    def get_gap_to_floor(self, floor):
        return floor - self._current_floor

    def go_to_floor(self, floor):
        gap = self.get_gap_to_floor(floor)
        if  gap > 0:
            self.set_direction(DIRECTION_UP)
            self.set_status(OCCUPIED)
            for i in range(gap):
                print('Reaching floor {}'.format(self._current_floor + i))
                self.set_floor(self._current_floor + i)
                time.sleep(10)

class Elevator_Operator(object):
    def __init__(self, no_of_elevator):
        self.elv_list = self._create_elevators(no_of_elevator)

    def _create_elevators(self, no_of_elevator):
        elv_list = []
        for i in range(no_of_elevator):
            elv = Elevator(i)
            elv_list.append(elv)
        return elv_list

    def choose_elevator(self, floor):
        elv_dict = {}
        gap_list = []
        for elv in self.elv_list:
            gap, is_direction = elv.is_available_for_pickup(floor)
            if is_direction:
                gap_list.append(gap)

            elv_dict.update({elv.get_elevator_name(): gap})

        return elv.get