''' Unit test for the AgentSociety class '''

import unittest
import sys
sys.path.append('../')
from self.agents.agent_society import AgentSociety

class TestAgentSociety(unittest.TestCase):
    ''' A bunch of unit tests that test the basic functionality of the AgentSociety
    class '''

    def test_get_instance(self):
        ''' Verify that the object gets instantiated correctly '''
        test_society = AgentSociety.get_instance()
        self.assertEqual(type(test_society), AgentSociety)


if __name__ == '__main__':
    unittest.main()
