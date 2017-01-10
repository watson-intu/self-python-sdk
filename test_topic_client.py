
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
from sensor_manager import SensorManager
from camera_sensor import CameraSensor
from microphone_sensor import MicrophoneSensor
from gesture_manager import GestureManager
from speech_gesture import SpeechGesture
from example_agent import ExampleAgent
from agent_society import AgentSociety

import multiprocessing
import thread
import time
import uuid

def run_thread(self, threadName):
		print "Thread is running!!"
		sensor = CameraSensor(str(uuid.uuid4()), "Camera", "VideoData", "image/jpeg")
		mic = MicrophoneSensor(str(uuid.uuid4()), "Microphone", "AudioData", "audio/L16;rate=16000;channels=1")
		gesture = SpeechGesture("tts", str(uuid.uuid4()))
		agent = ExampleAgent('ExampleAgent', str(uuid.uuid4()))
		while TopicClient.get_instance().isConnected() == False:
			print "Topic client not connected yet!"
			time.sleep(1)
		SensorManager.get_instance().subscribe()
		GestureManager.get_instance().subscribe()
		AgentSociety.get_instance().subscribe()
		SensorManager.get_instance().add_sensor(sensor, True)
		SensorManager.get_instance().add_sensor(mic, True)
		GestureManager.get_instance().add_gesture(gesture, True)
		AgentSociety.get_instance().add_agent(agent, False)

if __name__ == '__main__':
	import sys

	from twisted.python import log
	from twisted.internet import reactor
	try:
		log.startLogging(sys.stdout)
		headers = {'selfId': '', 'token': ''}
		topic = TopicClient.start_instance('127.0.0.1', 9443, headers)
		TopicClient.get_instance().setHeaders("", "")
#		p = multiprocessing.Process(target=run_thread, args=(topic,headers))
#		p.start()
		thread.start_new_thread(run_thread, (topic, headers))
		topic.start()
	except KeyboardInterrupt:
		thread.exit()
