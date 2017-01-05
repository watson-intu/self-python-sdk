
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
from twisted.internet import reactor
import json

class WebSocket(WebSocketClientProtocol):

	def onConnect(self, response):
		print("Connected!")

	def onOpen(self):
		print("Websocket connection opened")
		from topic_client import TopicClient
		TopicClient.get_instance().is_connected = True
		TopicClient.get_instance().web_socket_instance = self

	def onMessage(self, payload, isBinary):
		msg = format(payload.decode('utf-8'))
		data = json.loads(msg)
		from topic_client import TopicClient
		TopicClient.get_instance().onMessage(data)

	def onClose(self, wasClean, code, reason):
		print("Websocket connection closed: {0}".format(reason))

	@classmethod
	def send(self, data):
		print "SENDING OVER TO WEB SOCKET"
		protocol = WebSocket()
		print str(data).encode('utf8')
		protocol.sendMessage(str(data).encode('utf8'))
#		reactor.callFromThread(protocol.sendMessage, protocol, str(data).encode('utf8'))
