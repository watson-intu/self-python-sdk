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

import collections
import json
from self.topics.topic_client import TopicClient

class AgentSociety(object):
    ''' Represents a collection of agents running at a given time '''

    __instance = None

    def __init__(self):
        self.agent_map = collections.defaultdict(set)
        self.overrides_map = collections.defaultdict(set)

    @staticmethod
    def get_instance():
        ''' Return a singleton instance of the society '''
        if AgentSociety.__instance is None:
            AgentSociety.__instance = AgentSociety()
        return AgentSociety.__instance

    def on_event(self, data):
        ''' Callback that can add or remove proxy agents to and from the
        society '''
        error = False
        payload = json.loads(data)
        if payload['agentId'] not in self.agent_map:
            print "Could not find agent id: " + payload['agentId']
            error = True
        elif payload['event'] == 'start_agent':
            self.agent_map[payload['agentId']].on_start()
        elif payload['event'] == 'stop_agent':
            self.agent_map[payload['agentId']].on_stop()

        if error:
            data = {}
            data['failed_event'] = payload['event']
            data['event'] = 'error'
            TopicClient.get_instance().publish('agent-society', data, False)

    def subscribe(self):
        ''' Subscribe to the agent-society topic '''
        TopicClient.get_instance().subscribe('agent-society', self.on_event)

    def add_agent(self, agent, override):
        ''' Add an agent to this society. The society takes ownership of the
        agent '''
        if agent.get_agent_id not in self.agent_map:
            data = {}
            data['event'] = 'add_agent_proxy'
            data['agentId'] = agent.get_agent_id()
            data['name'] = agent.get_agent_name()
            data['override'] = override
            TopicClient.get_instance().publish('agent-society', data, False)
            self.agent_map[agent.get_agent_id()] = agent
            self.overrides_map[agent.get_agent_id()] = override

    def remove_agent(self, agent):
        ''' Remove an agent from this society '''
        if agent.get_agent_id in self.agent_map:
            self.overrides_map.remove(agent.get_agent_id())
            self.agent_map.remove(agent.get_agent_id())
            data = {}
            data['event'] = 'remove_agent_proxy'
            data['agentId'] = agent.get_agent_id()
            TopicClient.get_instance().publish('agent-society', data, False)

    def shutdown(self):
        ''' Unsubscribe from the agent-society topic '''
        TopicClient.get_instance().unsubscribe('agent-society')
