import unittest, time
from Elevator.Elevator import Elevator

class ElevatorTest(unittest.TestCase):
    def setUp(self):
        self.elevator = Elevator('1')
    def test_constructor(self):
        self.assertTrue(self.elevator.get_elevator_name(), 'Elevator 1')

    def test_set_load(self):
        self.elevator.set_load(5)
        self.assertTrue(self.elevator.get_load(), 5)

if __name__ == '__main__':
    unittest.main()