# Copyright 2022 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from xml.etree.ElementTree import TreeBuilder
import yaml
import requests
import json
import math
from urllib.error import HTTPError

class CaatoAPI:
    def __init__(self, prefix:str, config_file, cleaning_task_prefix="" , timeout=5.0, debug=True):
        #adding url prefix manually
        self.prefix = prefix
        self.debug = debug
        self.timeout = timeout

        data = self.data()
        if data is not None:
            print("[ClientAPI] successfully able to query API server")
            self.connected = True
        else:
            print("[ClientAPI] unable to query API server")
            self.connected = False

        print(config_file)
        # self.connected = True
        with open(config_file, "r") as f:
            config_yaml = yaml.safe_load(f)

        # These configs are provided in the yaml file

        # Sam: I will test each one without it and slowly phase it out
        #      currently, I'm leaving it here so the program doesn't break

        self.mock_clean_path = config_yaml["mock_clean_path"]
        self.mock_dock_path = config_yaml["mock_dock_path"]
        self.dock_position = config_yaml["dock_position"]
        self.mock_location = config_yaml["mock_location"]
        self.mock_robot_map_name = config_yaml["mock_robot_map_name"]

        self.is_mock_cleaning = False
        self.is_mock_docking = False
        self.task_wp_idx = 0
        print("[TEST ECOBOT CLIENT API] successfully setup mock client api class")

    def data(self):
        url = self.prefix + f"/"
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            if self.debug:
                print(f"[def data] - Response: {response.json()}")
            return response.json()
        except HTTPError as http_err:
            print(f"[def data] - HTTP error: {http_err}")
        except Exception as err:
            print(f"[def data] - Other error: {err}")
        return None

    def online(self):
        return self.connected

    def current_map(self):
        print(f"[TEST CLIENT API] return testing map: {self.mock_robot_map_name}")
        return self.mock_robot_map_name

    def position(self):
        ''' Returns [x, y, theta] expressed in the robot's coordinate frame or None'''
        url = self.prefix + f"/position"
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            if self.debug:
                print(f"[def position] - Response: {data}")
            x = data['pose_x']
            y = data['pose_y']
            angle = data['pose_theta']
            return [x, y, angle]
        except HTTPError as http_err:
            print(f"[def position] - HTTP error: {http_err}")
        except Exception as err:
            print(f"[def position] - Other error: {err}")
        return None
        # ''' Returns [x, y, theta] expressed in the robot's coordinate frame or None'''
        # if self.is_mock_cleaning:
        #     print(f"[TEST CLIENT API] provide mock cleaning position")
        #     return self.mock_clean_path[self.task_wp_idx]
        # elif self.is_mock_docking:
        #     print(f"[TEST CLIENT API] provide mock docking position")
        #     return self.mock_dock_path[self.task_wp_idx]
        # print(f"[TEST CLIENT API] provide position [{self.mock_location}]")
        # return self.mock_location

    def navigate(self, pose, map_name:str):
        ''' Here pose is a list containing (x,y,theta) where x and y are in grid
            coordinate frame and theta is in degrees. This functions should
            return True if the robot received the command, else False'''
        assert(len(pose) > 2)
        # self.mock_location = pose
        # print(f"[TEST CLIENT API] moved to mock location {pose}")
        # return True

        url = self.prefix + f"/navigate"
        data = {}
        data["nav_goal_x"] = pose[0]
        data["nav_goal_y"] = pose[1]
        data["nav_goal_z"] = pose[2]
        try:
            response = requests.post(url, timeout=self.timeout, json=data)
            response.raise_for_status()
            data = response.json()
            # if self.debug:
            #     print(f"[def position] - Response: {data}")
            # x = data['pose_x']
            # y = data['pose_y']
            # angle = data['pose_theta']
            return True
        except HTTPError as http_err:
            print(f"[def position] - HTTP error: {http_err}")
        except Exception as err:
            print(f"[def position] - Other error: {err}")
        return False

    def navigate_to_waypoint(self, waypoint_name, map_name):
        ''' Ask the robot to navigate to a preconfigured waypoint on a map.
            Returns True if the robot received the command'''
        print(f"[TEST CLIENT API] moved to mock waypoint {waypoint_name}")
        self.is_mock_docking = True
        return True

    def start_task(self, name:str, map_name:str):
        ''' Returns True if the robot has started the generic task, else False'''
        print(f"[TEST CLIENT API] Start mock task : {name}")
        if not self.is_mock_docking:
            self.is_mock_cleaning = True
        return True

    def pause(self):
        print(f"Pause Robot")
        url = self.prefix + f"/pause_navigation"
        data = {}
        try:
            response = requests.post(url, timeout=self.timeout, json=data)
            response.raise_for_status()
            data = response.json()
            # if self.debug:
            #     print(f"[def position] - Response: {data}")
            # x = data['pose_x']
            # y = data['pose_y']
            # angle = data['pose_theta']
            return True
        except HTTPError as http_err:
            print(f"[def position] - HTTP error: {http_err}")
        except Exception as err:
            print(f"[def position] - Other error: {err}")
        return False

    def resume(self):
        print(f"resume Robot")
        url = self.prefix + f"/resume_navigation"
        data = {}
        try:
            response = requests.post(url, timeout=self.timeout, json=data)
            response.raise_for_status()
            data = response.json()
            # if self.debug:
            #     print(f"[def position] - Response: {data}")
            # x = data['pose_x']
            # y = data['pose_y']
            # angle = data['pose_theta']
            return True
        except HTTPError as http_err:
            print(f"[def position] - HTTP error: {http_err}")
        except Exception as err:
            print(f"[def position] - Other error: {err}")
        return False

    def stop(self):
        ''' Returns true if robot was successfully stopped; else False'''
        print(f"Stop Robot")
        url = self.prefix + f"/stop"
        data = {}
        try:
            response = requests.post(url, timeout=self.timeout, json=data)
            response.raise_for_status()
            data = response.json()
            # if self.debug:
            #     print(f"[def position] - Response: {data}")
            # x = data['pose_x']
            # y = data['pose_y']
            # angle = data['pose_theta']
            return True
        except HTTPError as http_err:
            print(f"[def position] - HTTP error: {http_err}")
        except Exception as err:
            print(f"[def position] - Other error: {err}")
        return False

    def navigation_completed(self):
        url = self.prefix + f"/navigation_status"
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            if self.debug:
                print(f"[def data] - Response: {response.json()}")
            data = response.json()
            if data["navigation_status_code"] == 3:
                return True
            elif data["navigation_status_code"] == 1 or data["navigation_status_code"] == 0:
                return False
        except HTTPError as http_err:
            print(f"[def data] - HTTP error: {http_err}")
        except Exception as err:
            print(f"[def data] - Other error: {err}")
        return False

    def task_completed(self):
        ''' For ecobots the same function is used to check completion of navigation & cleaning'''
        self.task_wp_idx += 1
        if self.is_mock_docking:
            if self.task_wp_idx < len(self.mock_dock_path):
                print(f"[TEST CLIENT API] Mock nav/dock task in process")
                return False
            else:
                self.task_wp_idx = 0
                self.is_mock_docking = False
                self.mock_location = self.dock_position
                print(f"[TEST CLIENT API] Mock nav/dock task COMPLETED")
                return True
        else:
            if self.task_wp_idx < len(self.mock_clean_path):
                print(f"[TEST CLIENT API] MOCK CLEANING in process")
                return False
            else:
                self.task_wp_idx = 0
                self.is_mock_cleaning = False
                print(f"[TEST CLIENT API] MOCK CLEANING completed")
                return True

    def battery_soc(self):
        print(f"[TEST CLIENT API] get mock battery 100%")
        return 1.0

    def set_cleaning_mode(self, cleaning_config:str):
        print(f"[TEST CLIENT API] Set mock CLEANING MODE: {cleaning_config}")
        return True

    def is_charging(self):
        """Check if robot is charging, will return false if not charging, None if not avail"""
        dx, dy, _ = self.dock_position
        x, y, _= self.mock_location
        if (abs(x-dx) < 5.0 and abs(y-dy) < 5.0):
            print(f"[TEST CLIENT API] Mock robot at dock, is charging")
            return True
        return False

    def is_localize(self):
        return True
