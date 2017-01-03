
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

from autobahn.twisted.websocket import WebSocketClientFactory, \
	connectWS
from topic_client import TopicClient

if __name__ == '__main__':
	import sys

	from twisted.python import log
	from twisted.internet import reactor

	log.startLogging(sys.stdout)
	headers = {'selfId': '', 'token': ''}

	factory = WebSocketClientFactory(u"ws://127.0.0.1:9443/stream", headers=headers)
	factory.protocol = TopicClient
	

	connectWS(factory)
	reactor.run()