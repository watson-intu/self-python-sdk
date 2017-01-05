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

class CameraSensor(Sensor):

	def __init__(self, sensor_id, sensor_name, data_type, binary_type):
		super(self.__class__, self).__init__(sensor_id, sensor_name, data_type, binary_type)
		
	def on_start(self):
		print "Camera Sensor has started!"
		return True

	def on_stop(self):
		print "Camera Sensor has stopped!"
		return True

	def on_pause(self):
		print "Camera Sensor has paused!"
		self.is_paused = True

	def on_resume(self):
		print "Camera Sensor has resumed!"
		self.is_paused = False