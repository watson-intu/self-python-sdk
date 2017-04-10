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

from self.sensors.sensor import Sensor
from self.topics.topic_client import TopicClient

import collections
import json
import threading

class SensorManager(object):

	__instance_lock = threading.Lock()
	__instance = None

	def __init__(self):		
		self.sensor_map = collections.defaultdict(set)
		self.overrides_map = collections.defaultdict(set)

	@classmethod
	def get_instance(cls):
		if not cls.__instance:
			with cls.__instance_lock:
				if not cls.__instance:
					print "Sensor Manager has been instantiated!"
					cls.__instance = cls()
		return cls.__instance

	def on_event(self, data):
		error = False
		payload = json.loads(data)
		if payload['sensorId'] not in self.sensor_map:
			print "Failed to find sensor: " + payload['sensorId']
			error = True
		elif payload['event'] == 'start_sensor':
			self.sensor_map[payload['sensorId']].on_start()
		elif payload['event'] == 'pause_sensor':
			self.sensor_map[payload['sensorId']].on_pause()
		elif payload['event'] == "resume_sensor":
			self.sensor_map[payload['sensorId']].on_resume()

		if error:
			data = {}
			data['failed_event'] = payload['event']
			data['event'] = 'error'
			TopicClient.get_instance().publish('sensor-manager', data, False)


	def subscribe(self):
		TopicClient.get_instance().subscribe("sensor-manager", self.on_event)

	def add_sensor(self, sensor, override):
		if sensor.get_sensor_id() not in self.sensor_map:
			data = {}
			data['event'] = 'add_sensor_proxy'
			data['sensorId'] = sensor.get_sensor_id()
			data['name'] = sensor.get_sensor_name()
			data['data_type'] = sensor.get_data_type()
			data['binary_type'] = sensor.get_binary_type()
			data['override'] = override
			TopicClient.get_instance().publish('sensor-manager', data, False)
			self.sensor_map[sensor.get_sensor_id()] = sensor
			self.overrides_map[sensor.get_sensor_id()] = override
			print "adding sensor id: " + sensor.get_sensor_id()

	def is_registered(self, sensor):
		if sensor.get_sensor_id() in self.sensor_map:
			return True
		return False

	def remove_sensor(self, sensor):
		if sensor.get_sensor_id() in self.sensor_map:
			self.sensor_map.remove(sensor.get_sensor_id())
			self.override_map.remove(sensor.get_sensor_id())
			data = {}
			data['event'] = 'remove_sensor_proxy'
			data['sensorId'] = sensor.get_sensor_id()
			TopicClient.get_instance().publish('sensor-manager', data, False)

	def send_data(self, sensor, data):
		if self.is_registered(sensor):
			TopicClient.get_instance().publish_binary('sensor-proxy-' + sensor.get_sensor_id(), data, False)
		else:
			print "SendData() invoked on unregistered sensor: " + sensor.get_sensor_id()

	def shutdown(self):
		TopicClient.get_instance().unsubscribe('sensor-manager')

	def find_sensor(self, data):
		for k,v in self.sensor_map.iteritems():
			if v.get_data_type() == data:
				return v
