import logging
import os

import requests

from function.base import BaseFunction
from function.factory import FunctionRegisterError

log = logging.getLogger('plugin weather')


class BusPathFunction(BaseFunction):

    def __init__(self):
        self.key = os.getenv('PLUGIN_WEATHER_KEY', None)
        if self.key is None:
            raise FunctionRegisterError('Not set PLUGIN_WEATHER_KEY')
        super().__init__()

    def declare(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": "get_bus_path",
                "description": "获取起点到终点的公交线路规划",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "start": {
                            "type": "string",
                            "description": "起点",
                        },
                        "end": {
                            "type": "string",
                            "description": "终点",
                        },
                    },
                    "required": ["start", "end"],
                },
            }
        }

    def execute(self, function_args) -> str:
        """Get the current weather in a given location"""
        start = function_args.get("start")
        end = function_args.get("end")

        start_city_code_url = f'https://restapi.amap.com/v3/geocode/geo?key={self.key}&address={start}'
        end_city_code_url = f'https://restapi.amap.com/v3/geocode/geo?key={self.key}&address={end}'
        start_city_code_resp = requests.get(start_city_code_url)
        end_city_code_resp = requests.get(end_city_code_url)
        if start_city_code_resp.status_code == 200 and end_city_code_resp.status_code == 200:
            start_city_data = start_city_code_resp.json()
            end_city_data = end_city_code_resp.json()
            start_city_code = start_city_data['geocodes'][0]['citycode']
            start_location = start_city_data['geocodes'][0]['location']
            end_city_code = end_city_data['geocodes'][0]['citycode']
            end_location = end_city_data['geocodes'][0]['location']

            path_info_url = f'https://restapi.amap.com/v5/direction/transit/integrated?key={self.key}&origin={start_location}&destination={end_location}&city1=0571&city2=0571'
            path_resp = requests.get(path_info_url)
            if path_resp.status_code == 200:
                return path_resp.text

        return '规划公交线路信息失败'
