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

from sensor import Sensor
from topic_client import TopicClient

import collections

class SensorManager:

	__instance = None

	def __init__(self):		
		self.sensor_map = collections.defaultdict(set)
		self.overrides_map = collections.defaultdict(set)

	@staticmethod
	def get_instance():
		if SensorManager.__instance == None:
			SensorManager.__instance = SensorManager()
		return SensorManager.__instance

	def on_event(payload):
		print payload

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
