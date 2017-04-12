'''
Copyright 2016 IBM All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

class Agent(object):
    ''' An agent in the Intu universe is an entity that can subscribe to
    the blackboard for objects it is interested in. Additionally, they
    can subscribe to different levels of events for those objects
    '''
    def __init__(self, agent_name, agent_id):
        self.agent_name = agent_name
        self.agent_id = agent_id

    def get_agent_name(self):
        ''' Return the name of the agent '''
        if self.agent_name is None or self.agent_name == '':
            raise Exception('The agent_name should not be blank or None')
        return self.agent_name

    def get_agent_id(self):
        ''' Return the ID of the agent '''
        if self.agent_id is None or self.agent_id == '':
            raise Exception('The agent_id should not be blank or None')
        return self.agent_id
