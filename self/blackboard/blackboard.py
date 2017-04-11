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
from self.blackboard.subscriber import Subscriber
from self.blackboard.thing import Thing
from self.blackboard.thing import ThingEventType
from self.blackboard.thing import ThingEvent

class Blackboard(object):
    ''' Represents the central publish/subscribe system for all agents,
    classifiers, and extractors '''

    __instance = None

    def __init__(self):
        self.subscription_map = collections.defaultdict(set)
        self.thing_map = collections.defaultdict(set)

    @staticmethod
    def get_instance():
        ''' Return the Singleton instance of the blackboard '''
        if Blackboard.__instance is None:
            Blackboard.__instance = Blackboard()
        return Blackboard.__instance

    def on_event(self, data):
        ''' Invoke this method to pass an event to all subscribers for a given
        object type '''
        error = False
        payload = json.loads(data)
        thing = Thing()
        thing_event = ThingEvent()
        thing_event.set_event_type(ThingEventType.NONE)
        thing_event.set_event(payload)
        if payload['event'] == 'add_object':
            thing_event.set_event_type(ThingEventType.ADDED)
            thing_event.set_thing(payload['thing'])
            thing.deserialize(payload['thing'])
            if 'parent' in payload:
                thing.set_parent(payload['parent'])
            thing_event.set_thing(thing)
            self.thing_map[thing.get_guid()] = thing
        elif payload['event'] == 'remove_object':
            thing_event.set_event_type(ThingEventType.REMOVED)
            if payload['thing_guid'] in self.thing_map:
                self.thing_map.remove(payload['thing_guid'])
        elif payload['event'] == 'set_object_state':
            if payload['thing_guid'] in self.thing_map:
                self.thing_map[payload['thing_guid']].set_state(payload['state'])
            else:
                thing.deserialize(payload['thing'])
                if 'parent' in payload:
                    thing.set_parent(payload['parent'])
                thing_event.set_thing(thing)
                self.thing_map[payload['thing_guid']] = thing
        elif payload['event'] == 'set_object_importance':
            if payload['thing_guid'] in self.thing_map:
                payload['thing_guid'].set_importance(payload['importance'])

        if thing_event.get_event_type() is not ThingEventType.NONE:
            for k, v in self.subscription_map.iteritems():
                for key, value in v.iteritems():
                    if payload['type'] == key:
                        for i in value:
                            if thing_event.get_event_type() == i.event:
                                i.callback(payload)


    def subscribe_to_type(self, thing, thing_event, path, callback):
        ''' Subscribe to any objects of a given type that get put on the
        blackboard '''
        if path not in self.subscription_map:
            TopicClient.get_instance().subscribe(path + 'blackboard', self.on_event)
            self.subscription_map[path] = collections.defaultdict(set)

        if thing not in self.subscription_map[path]:
            data = {}
            data['event'] = 'subscribe_to_type'
            data['type'] = thing
            data['event_mask'] = thing_event
            TopicClient.get_instance().publish(path + 'blackboard', data, False)
            self.subscription_map[path][thing] = []

        self.subscription_map[path][thing].append(Subscriber(callback, thing_event, path))

    def unsubscribe_to_type(self, thing, callback, path):
        ''' Unsubscribe from a given type of objects that get put on the
        blackboard '''
        if path in self.subscription_map:
            if thing in self.subscription_map[path]:
                for subscription in self.subscription_map[path][thing]:
                    if subscription.callback == callback:
                        self.subscription_map[path][thing].remove(subscription)
                        break

                if len(self.subscription_map[path][thing]) == 0:
                    self.subscription_map[path].remove(thing)

            if thing not in self.subscription_map[path]:
                data = {}
                data['event'] = 'unsubscribe_from_type'
                data['type'] = thing
                TopicClient.get_instance().publish(path + 'blackboard', data, False)

    def add_thing(self, thing, path):
        ''' Add a concept to this blackboard, which will be automatically
        connected to other concepts to produce a goal in the end '''
        data = {}
        data['event'] = 'add_object'
        data['type'] = thing.get_type()
        data['thing'] = thing.serialize()
        if thing.get_parent():
            data['parent'] = thing.get_parent()
        TopicClient.get_instance().publish(path + 'blackboard', data, False)

    def remove_thing(self, thing, path):
        ''' Remove a specific thing from the blackboard '''
        data = {}
        data['event'] = 'remove_object'
        data['thing_guid'] = thing.get_guid()
        TopicClient.get_instance().publish(path + 'blackboard', data, False)

    def set_state(self, thing, state, path):
        ''' Publish a given state to a given path on the blackboard '''
        data = {}
        data['event'] = 'set_object_state'
        data['thing_guid'] = thing.get_guid()
        data['state'] = state
        TopicClient.get_instance().publish(path + 'blackboard', data, False)

    def set_importance(self, thing, importance, path):
        ''' Publish a given level of importance to a given path on the
        blackboard '''
        data = {}
        data['event'] = 'set_object_importance'
        data['thing_guid'] = thing.get_guid()
        data['importance'] = importance
        TopicClient.get_instance().publish(path + 'blackboard', data, False)
