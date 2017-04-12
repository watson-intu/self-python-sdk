''' Unit test for the Agent class '''

import unittest
import sys
sys.path.append('../')
from self.agents.agent import Agent

class TestAgent(unittest.TestCase):
    ''' A bunch of unit tests that test the basic functionality of the Agent
    class '''

    def test_agent_init(self):
        ''' Test the basic initialization of an agent '''
        test_agent = Agent('test_agent', 1)
        self.assertEqual(test_agent.get_agent_name(), 'test_agent')
        self.assertEqual(test_agent.get_agent_id(), 1)

    def test_data_name(self):
        ''' Do not allow empty or None names to go unnoticed '''
        test_agent = Agent(None, 1)
        with self.assertRaises(Exception):
            test_agent.get_agent_name()

        test_agent_2 = Agent('', 1)
        with self.assertRaises(Exception):
            test_agent_2.get_agent_name()

    def test_data_id(self):
        ''' Do not allow empty or None ids to go unnoticed '''
        test_agent = Agent('test_agent', None)
        with self.assertRaises(Exception):
            test_agent.get_agent_id()

        test_agent_2 = Agent('test_agent', '')
        with self.assertRaises(Exception):
            test_agent_2.get_agent_id()


if __name__ == '__main__':
    unittest.main()
