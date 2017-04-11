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

class Sensor(object):
    ''' Represents all sensors that can receive some type of data from an
    external source, e.g. video camera, microphone, or data through a
    connected socket '''

    def __init__(self, sensor_id, sensor_name, data_type, binary_type):
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        self.data_type = data_type
        self.binary_type = binary_type

    def get_sensor_id(self):
        return self.sensor_id

    def get_sensor_name(self):
        return self.sensor_name

    def get_data_type(self):
        return self.data_type

    def get_binary_type(self):
        return self.binary_type
