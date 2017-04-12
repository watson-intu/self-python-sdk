''' Unit test for the Blackboard Thing class '''

import unittest
import sys
sys.path.append('../')
from self.blackboard.thing import Thing
from self.blackboard.thing import ThingEvent

class TestThing(unittest.TestCase):
    ''' A bunch of unit tests that test the basic functionality of the Thing
    class '''

    def test_get_instance(self):
        ''' Verify that the object gets instantiated correctly with default
        values '''
        test_thing = Thing()
        self.assertEqual(test_thing.get_type(), 'IThing')

        # Because the ThingCategory.PERCEPTION is 0
        self.assertEqual(test_thing.get_category(), 0)
        self.assertEqual(test_thing.get_state(), 'ADDED')

    def test_mutation(self):
        ''' Verify that the mutators are able to correctly set values '''
        test_thing = Thing()
        self.assertEqual(test_thing.get_type(), 'IThing')
        test_thing.set_type('Text')
        self.assertEqual(test_thing.get_type(), 'Text')

    def test_serialize(self):
        ''' Verify that the serialization returns correct data in the correct
        format '''
        test_thing = Thing()
        self.assertEqual(test_thing.serialize()['Type_'], 'IThing')
        self.assertEqual(test_thing.serialize()['m_eCategory'], 0)


if __name__ == '__main__':
    unittest.main()
