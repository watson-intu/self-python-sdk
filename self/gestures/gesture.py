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

class Gesture(object):
    ''' Represents objects that are placed onto the blackboard when we
    need Intu to perform a basic task, such as say anything '''

    def __init__(self, gesture_id, instance_id):
        self.gesture_id = gesture_id
        self.instance_id = instance_id

    def get_gesture_id(self):
        ''' Return the gesture ID associated with this gesture '''
        if self.gesture_id is None or self.gesture_id == '':
            raise Exception('gesture_id should not be empty or None')
        return self.gesture_id

    def get_instance_id(self):
        ''' Return the instance ID associated with this gesture '''
        if self.instance_id is None or self.instance_id == '':
            raise Exception('instance_id should not be empty or None')
        return self.instance_id
