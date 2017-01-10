
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
from ws4py.client.threadedclient import WebSocketClient

class WebSocket(WebSocketClient):

	def opened(self):
		print("Connected!")
		from topic_client import TopicClient
		TopicClient.get_instance().is_connected = True
		TopicClient.get_instance().web_socket_instance = self
		TopicClient.get_instance().isConnected()
		
	def closed(self, code, reason=None):
		print "Closed down", code, reason
		from topic_client import TopicClient
		TopicClient.get_instance().is_connected = False
		
	def received_message(self, payload):
		if payload.is_text:
			msg = payload.data.decode('utf-8')
			data = json.loads(msg)
			from topic_client import TopicClient
			TopicClient.get_instance().onMessage(data)
		else:
			print "Cannot convert message returned to json!"
