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

import collections
import multiprocessing
import json

from topic_client import TopicClient
from gesture import Gesture

class GestureManager:

	__instance = None

	def __init__(self):
		self.gestures_map = collections.defaultdict(set)
		self.overrides_map = collections.defaultdict(set)


	@staticmethod
	def get_instance():
		if GestureManager.__instance == None:
			GestureManager.__instance = GestureManager()
		return GestureManager.__instance

	def add_gesture(self, gesture, override):
		if gesture.get_gesture_id() not in self.gestures_map:
			if gesture.on_start():
				data = {}
				data['event'] = 'add_gesture_proxy'
				data['gestureId'] = gesture.get_gesture_id()
				data['instanceId'] = gesture.get_instance_id()
				data['override'] = override
				TopicClient.get_instance().publish('gesture-manager', data, False)
				self.gestures_map[gesture.get_gesture_id()] = gesture
				self.overrides_map[gesture.get_gesture_id()] = override
				print "adding gesture id: " + gesture.get_gesture_id()

	def remove_gesture(self, gesture):
		if gesture.get_gesture_id() in self.gestures_map:
			if gesture.on_stop():
				data = {}
				self.gestures_map.remove(gesture.get_gesture_id())
				self.overrides_map.remove(gesture.get_gesture_id())
				data['event'] = 'remove_gesture_proxy'
				data['gestureId'] = gesture.get_gesture_id()
				data['instanceId'] = gesture.get_instance_id()
				TopicClient.get_instance().publish('gesture-manager', data, False)
		
	def on_event(self, data):
		error = False
		payload = json.loads(data)
		if payload['gestureId'] not in self.gestures_map:
			print "Failed to find gesture: " + payload['gestureId']
			error = True
		elif payload['event'] == 'execute_gesture':
			params = payload['params']
			self.gestures_map[payload['gestureId']].execute(params)
		elif payload['event'] == 'abort_gesture':
			self.gestures_map[payload['gestureId']].abort()

		if error:
			data = {}
			data['failed_event'] = payload['event']
			data['event'] = 'error'
			TopicClient.get_instance().publish('gesture-manager', data, False)

	def subscribe(self):
		TopicClient.get_instance().subscribe('gesture-manager', self.on_event)

	def on_gesture_done(self, gesture, error):
		data = {}
		data['event'] = 'execute_done'
		data['gestureId'] = gesture.get_gesture_id()
		data['instanceId'] = gesture.get_instance_id()
		data['error'] = error
		TopicClient.get_instance().publish('gesture-manager', data, False)