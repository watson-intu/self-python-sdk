''' Unit test for the Gesture class '''

import unittest
import sys
sys.path.append('../')
from self.gestures.gesture import Gesture

class TestGesture(unittest.TestCase):
    ''' A bunch of unit tests that test the basic functionality of the Gesture
    class '''

    def test_get_instance(self):
        ''' Verify that the object gets instantiated correctly with default
        values '''
        test_gesture = Gesture(1, 2)
        self.assertEqual(test_gesture.get_gesture_id(), 1)
        self.assertEqual(test_gesture.get_instance_id(), 2)

    def test_gesture_id_sanity(self):
        ''' Should not allow a blank or None gesture ID to go unnoticed '''
        test_gesture = Gesture(None, 2)
        with self.assertRaises(Exception):
            test_gesture.get_gesture_id()

        test_gesture = Gesture('', 2)
        with self.assertRaises(Exception):
            test_gesture.get_gesture_id()

    def test_instance_id_sanity(self):
        ''' Should not allow a blank or None instance ID to go unnoticed '''
        test_gesture = Gesture(1, None)
        with self.assertRaises(Exception):
            test_gesture.get_instance_id()

        test_gesture = Gesture(1, '')
        with self.assertRaises(Exception):
            test_gesture.get_instance_id()

if __name__ == '__main__':
    unittest.main()
