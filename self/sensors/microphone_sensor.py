'''
Copyright 2016 IBM All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import sys

from self.sensors.sensor import Sensor
from self.sensors.sensor_manager import SensorManager

import pyaudio

class MicrophoneSensor(Sensor):
    ''' Collects audio data from the local device '''

    def __init__(self, sensor_id, sensor_name, data_type, binary_type):
        super(self.__class__, self).__init__(sensor_id, sensor_name, data_type, binary_type)
        self.is_paused = False
        self.pyaudio = None
        self.stream = None

    def on_stream(self, in_data, frame_count, time_info, status):
        ''' Stub implementation to return the data with the PortAudio return code '''
        if self.is_paused is False:
            SensorManager.get_instance().send_data(self, in_data)
        return in_data, pyaudio.paContinue

    def on_start(self):
        ''' Start streaming '''
        self.pyaudio = pyaudio.PyAudio()
        self.stream = self.pyaudio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1600, stream_callback=self.on_stream)
        return True

    def on_stop(self):
        ''' Terminate the PyAudio streaming session '''
        print "Microphone Sensor has stopped!"
        self.pyaudio.terminate()
        return True

    def on_pause(self):
        ''' Pause the streaming '''
        print "Microphone Sensor has paused!"
        self.is_paused = True

    def on_resume(self):
        ''' Resume the paused streaming '''
        print "Microphone Sensor has resumed!"
        self.is_paused = False
