''' Unit test for the Sensor class '''

import unittest
import sys
sys.path.append('../')
from self.sensors.sensor import Sensor

class TestSensor(unittest.TestCase):
    ''' A bunch of unit tests that test the basic functionality of the Sensor
    class '''

    def test_sensor_initialization(self):
        ''' Initialize the sensor and verify that the attributes get populated
        correctly '''
        test_sensor = Sensor(1, 'test_sensor', 'text', False)
        self.assertEqual(test_sensor.get_sensor_id(), 1)
        self.assertEqual(test_sensor.get_sensor_name(), 'test_sensor')
        self.assertEqual(test_sensor.get_data_type(), 'text')
        self.assertEqual(test_sensor.get_binary_type(), False)

    def test_nonone_id(self):
        ''' The ID should not be None when initializing a sensor '''
        test_sensor = Sensor(None, 'test_sensor', 'text', False)
        with self.assertRaises(Exception):
            test_sensor.get_sensor_id()

    def test_noblank_id(self):
        ''' The ID should not be blank when initializing a sensor '''
        test_sensor = Sensor('', 'test_sensor', 'text', False)
        with self.assertRaises(Exception):
            test_sensor.get_sensor_id()

    def test_nonone_name(self):
        ''' The name should not be None when initializing a sensor '''
        test_sensor = Sensor(1, None, 'text', False)
        with self.assertRaises(Exception):
            test_sensor.get_sensor_name()

    def test_noblank_name(self):
        ''' The ID should not be blank when initializing a sensor '''
        test_sensor = Sensor(1, '', 'text', False)
        with self.assertRaises(Exception):
            test_sensor.get_sensor_name()

    def test_nonone_datatype(self):
        ''' The data type should not be None when initializing a sensor '''
        test_sensor = Sensor(1, 'test_sensor', None, False)
        with self.assertRaises(Exception):
            test_sensor.get_data_type()

    def test_noblank_datatype(self):
        ''' The data type should not be blank when initializing a sensor '''
        test_sensor = Sensor(1, 'test_sensor', None, False)
        with self.assertRaises(Exception):
            test_sensor.get_data_type()

    def test_nonone_binarytype(self):
        ''' The binary type should not be None when initializing a sensor '''
        test_sensor = Sensor(1, 'test_sensor', 'test', None)
        with self.assertRaises(Exception):
            test_sensor.get_binary_type()

    def test_noblank_binarytype(self):
        ''' The binary type should not be blank when initializing a sensor '''
        test_sensor = Sensor(1, 'test_sensor', 'test', '')
        with self.assertRaises(Exception):
            test_sensor.get_binary_type()


if __name__ == '__main__':
    unittest.main()
