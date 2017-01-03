
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

from autobahn.twisted.websocket import WebSocketClientProtocol

class TopicClient(WebSocketClientProtocol):
	def onConnect(self, response):
		print("Connected!")

	def onOpen(self):
		print("Websocket connection opened")

	def send(self, msg):
		print("Sending the following message: " + msg)
		self.sendMessage(msg)

	def onMessage(self, payload, isBinary):
		print("Text message received: {0}".format(payload.decode('utf-8')))

	def onClose(self, wasClean, code, reason):
		print("Websocket connection closed: {0}".format(reason))

	def setHeaders(self, id, token):
		self.self_id = id
		self.token = token
		print("self_id is " + self.self_id + ", and token is: " + self.token)


