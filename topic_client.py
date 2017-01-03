
# Copyright 2016 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import collections
from autobahn.twisted.websocket import WebSocketClientProtocol

class TopicClient(WebSocketClientProtocol):

	def __init__(self):
		self.self_id = ""
		self.token = ""
		self.subscription_map = collections.defaultdict(set)

	def onConnect(self, response):
		print("Connected!")

	def onOpen(self):
		print("Websocket connection opened")

	def send(self, msg):
		data = json.load(msg)
		data["origin"] = self.self_id + "/."
		print("Sending the following message: " + data)
		self.sendMessage(data)

	def send_binary(self, msg, payload):
		data = json.load(msg)
		data['data'] = len(payload)
		data['origin'] = self.self_id + "/."
		header = json.dumps(data).encode('utf-8')
		frame = header + payload
		self.sendMessage(frame,binary=True)

	def onMessage(self, payload, isBinary):
		msg = format(payload.decode('utf-8'))
		data = json.loads(msg)
		print(data)
		if 'topic' not in data:
			return
		if data['topic'] in self.subscription_map:
			self.subscription_map.get(data['topic'])(data['data'])

	def onClose(self, wasClean, code, reason):
		print("Websocket connection closed: {0}".format(reason))

	def setHeaders(self, id, token):
		self.self_id = id
		self.token = token
		print("self_id is " + self.self_id + ", and token is: " + self.token)

	def subscribe(self, path, callback):
		if path not in self.subscription_map:
			self.subscription_map[path] = callback

		data = {}
		targets = [path]
		data['targets'] = targets
		data['msg'] = 'subscribe'
		self.send(data)

	def unsubscribe(self, path):
		if path in self.subscription_map:
			self.subscription_map.remove(path)
			data = {}
			targets = [path]
			data['targets'] = targets
			data['msg'] = 'unsubscribe'
			self.send(data)
			return True
		return False

	def publish(path, payload, persisted):
		data = {}
		targets = [path]
		data['targets'] = targets
		data['msg'] = 'publish_at'
		data['data'] = payload
		data['binary'] = False
		data['persisted'] = persisted
		self.send(data)

	def publish_binary(path, payload, persisted):
		data = {}
		targets = [path]
		data['targets'] = targets
		data['msg'] = 'publish_at'
		data['binary'] = True
		data['persisited'] = persisted
		self.send_binary(data, payload)
