import datetime
import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry


class TemperatureManager:
    def __init__(self):
        cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

        self.openmeteo_interface = openmeteo_requests.Client(session=retry_session)
        self.url = "https://marine-api.open-meteo.com/v1/marine"

    def hourly_data(self, longtitude: float, latitude: float, date: str):
        params = {
            "latitude": latitude,
            "longitude": longtitude,
            "hourly": "sea_surface_temperature",
            "start_date": date,
            "end_date": date,
            "timezone": "UTC",
        }
        responses = self.openmeteo_interface.weather_api(self.url, params=params)
        response = responses[0]

        hourly = response.Hourly()
        start_timestamp = hourly.Time()
        interval_seconds = hourly.Interval()

        temps = hourly.Variables(0).ValuesAsNumpy()
        num_points = len(temps)

        dates = [
            datetime.datetime.utcfromtimestamp(start_timestamp + interval_seconds * i).isoformat()
            for i in range(num_points)
        ]

        print(dates)
        print(temps)
        # hourly_data["sea_surface_temperature"] = hourly_sea_surface_temperature
        # print(hourly_data)
        # hourly_dataframe = pd.DataFrame(data=hourly_data)
        # print("\nHourly data\n", hourly_dataframe)


if __name__ == "__main__":
    tm = TemperatureManager()
    tm.hourly_data(10.2083435, 54.541664, "2025-09-13")
