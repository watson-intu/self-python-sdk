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

import uuid
import calendar
import time
import json

class ThingCategory(object):
    ''' Intu supports different types of things. Things belonging to different
    types are not attached to each other directly but rather a proxy is created
    and connected via GUID '''
    INVALID = -1
    PERCEPTION = 0
    AGENCY = 1
    MODEL = 2

class ThingEventType(object):
    ''' Represents different types of an event related to things such as
    whether a thing has been added, removed, or changed '''
    NONE = 0
    ADDED = 1
    REMOVED = 2
    STATE = 4
    IMPORTANCE = 8

class Thing(object):
    ''' Represents all objects that can be added to the blackboard '''

    def __init__(self):
        self.type = "IThing"
        self.category = ThingCategory.PERCEPTION
        self.guid = str(uuid.uuid4())
        self.importance = 1.0
        self.state = "ADDED"
        self.create_time = calendar.timegm(time.gmtime())
        self.life_span = 3600.0
        self.body = {}
        self.data_type = ""
        self.data = {}
        self.parent = ""

    def get_type(self):
        return self.type

    def set_type(self, a_type):
        self.type = a_type

    def get_category(self):
        return self.category

    def set_category(self, a_category):
        self.category = a_category

    def get_guid(self):
        return self.guid

    def set_guid(self, a_guid):
        self.guid = a_guid

    def get_importance(self):
        return self.importance

    def set_importance(self, a_importance):
        self.importance = a_importance

    def get_state(self):
        return self.state

    def set_state(self, a_state):
        self.state = a_state

    def get_create_time(self):
        return self.create_time

    def set_create_time(self, a_create_time):
        self.create_time = a_create_time

    def get_life_span(self):
        return self.life_span

    def set_life_span(self, a_life_span):
        self.life_span = a_life_span

    def get_body(self):
        return self.body

    def set_body(self, a_body):
        self.body = a_body

    def get_parent(self):
        return self.parent

    def set_parent(self, a_parent):
        self.parent = a_parent

    def serialize(self):
        ''' Convert the data into a map and return it '''
        data = {}
        if bool(self.body):
            for k, v in self.body.iteritems():
                data[k] = v

        data['Type_'] = self.type
        data['m_eCategory'] = self.category
        data['GUID_'] = self.guid
        data['m_fImportance'] = self.importance
        data['m_State'] = self.state
        data['m_fLifeSpan'] = self.life_span

        if self.data_type:
            data['m_DataType'] = self.data_type
            data['m_Data'] = self.data

        return data

    def deserialize(self, payload):
        ''' Read attributes from a map and associate the values to this thing '''
        self.body = payload
        self.type = str(payload['Type_'])
        self.category = str(payload['m_eCategory'])
        self.guid = str(payload['GUID_'])
        self.state = str(payload['m_State'])
        if 'm_fImportance' in payload:
            self.importance = str(payload['m_fImportance'])
        if 'm_CreateTime' in payload:
            self.create_time = str(payload['m_CreateTime'])
        if 'm_fLifeSpan' in payload:
            self.life_span = str(payload['m_fLifeSpan'])
        if 'm_DataType' in payload:
            self.data_type = str(payload['m_DataType'])
        if 'm_Data' in payload:
            self.data = str(payload['m_Data'])

class ThingEvent(object):
    ''' Represents an add, remove, or state change (and others) event
    that can happen to a thing '''

    def __init__(self):
        self.event_type = ""
        self.event = ""
        self.thing = ""

    def get_event_type(self):
        return self.event_type

    def set_event_type(self, a_event_type):
        self.event_type = a_event_type

    def get_event(self):
        return self.event

    def set_event(self, a_event):
        self.event = a_event

    def get_thing(self):
        return self.thing

    def set_thing(self, a_thing):
        self.thing = a_thing
