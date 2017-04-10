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

from gesture import Gesture
from sensor import Sensor
from sensor_manager import SensorManager
from gesture_manager import GestureManager

class SpeechGesture(Gesture):

	def __init__(self, gesture_id, instance_id):
		super(self.__class__, self).__init__(gesture_id, instance_id)

	def on_start(self):
		print "SpeechGesture has started!"
		return True

	def on_stop(self):
		print "SpeechGesture has stopped!"
		return True

	def execute(self, params):
		text = params['text']
		language = params['language']
		gender = params['gender']
		sensor = SensorManager.get_instance().find_sensor('AudioData')
		if sensor is not None:
			sensor.on_pause()
		print "SpeechGesture: " + text
		# TODO: Tell Gesture Manager you're done
		GestureManager.get_instance().on_gesture_done(self, False)
		if sensor is not None:
			sensor.on_resume()

		return True

	def abort(self):
		return True