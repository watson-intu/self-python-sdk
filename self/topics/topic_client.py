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

import json
import collections
import sys
import codecs
import time

from self.topics.web_socket import WebSocket

class TopicClient:
    ''' A client to make WebSocket connections to the TopicManager. This
    enables the user to access publish/subscribe events on the instance '''

    __instance = None

    def __init__(self, host, port, data):
        self.self_id = ""
        self.token = ""
        self.subscription_map = collections.defaultdict(set)
        self.is_connected = False
        self.host = host
        self.port = port
        self.headers = data
        self.web_socket_instance = None
        self.callback = None
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.reactor = WebSocket("ws://"+host+":"+str(port)+"/stream", headers=data, protocols=['http-only', 'chat'])
        print "Topic Client is instantiated!"

    @classmethod
    def get_instance(cls):
        ''' Sometimes the TopicClient needs to be re-instantiated '''
        if cls.__instance is None:
            print "Trying to re instantiated Topic Client for some reason..."
            cls.__instance = TopicClient()
        return cls.__instance

    @classmethod
    def start_instance(cls, host, port, data):
        ''' Return the Singleton TopicClient '''
        if cls.__instance is None:
            print "TopicClient Instantiated!"
            cls.__instance = TopicClient(host, port, data)
        return cls.__instance

    def set_callback(self, callback):
        ''' Set the callback method '''
        self.callback = callback

    def start(self):
        ''' Stub implementation of starting the WebSocket connection and run it
        forever '''
        self.reactor.connect()
        self.reactor.run_forever()

    def send(self, msg):
        ''' Send off the message via the WebSocket connection '''
        msg["origin"] = self.self_id + "/."
        msg = json.dumps(msg)
        if self.is_connected:
            self.web_socket_instance.send(str(msg).encode('utf8'),binary=False)

    def onMessage(self, data):
        ''' Handle incoming messages '''
        if 'topic' not in data:
            return
        if data['topic'] in self.subscription_map:
            self.subscription_map.get(data['topic'])(data['data'])

    def send_binary(self, payload, data):
        ''' Send binary payload via the WebSocket connection '''
        payload['data'] = len(data)
        payload['origin'] = self.self_id + "/."
        header = json.dumps(payload) + '\0'
        header = header.encode('utf8')
        frame = b''.join([header, data])
        if self.is_connected:
            self.web_socket_instance.send(frame, binary=True)
        else:
            print "Websocket not connected to send binary!"

    def isConnected(self):
        self.callback()
        return self.is_connected

    def setHeaders(self, id, token):
        self.self_id = id
        self.token = token

    def subscribe(self, path, callback):
        ''' Subscribe to a topic if possible '''
        if path not in self.subscription_map:
            self.subscription_map[path] = callback
        data = {}
        targets = [path]
        data["targets"] = targets
        data["msg"] = "subscribe"
        self.send(data)

    def unsubscribe(self, path):
        ''' Unsubscribe from a given topic '''
        if path in self.subscription_map:
            self.subscription_map.remove(path)
            data = {}
            targets = [path]
            data['targets'] = targets
            data['msg'] = 'unsubscribe'
            self.send(data)
            return True
        return False

    def publish(self, path, payload, persisted):
        ''' Publish data to the topic '''
        data = {}
        targets = [path]
        data['targets'] = targets
        data['msg'] = 'publish_at'
        data['data'] = str(json.dumps(payload))
        data['binary'] = False
        data['persisted'] = persisted
        self.send(data)

    def publish_binary(self, path, payload, persisted):
        ''' Publish binary data to the topic '''
        data = {}
        targets = [path]
        data['targets'] = targets
        data['msg'] = 'publish_at'
        data['binary'] = True
        data['persisited'] = persisted
        self.send_binary(data, payload)
