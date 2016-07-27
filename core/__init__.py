import json
import urllib
import urllib2
from core.utils import median


class Weather:
    baseurl = "https://query.yahooapis.com/v1/public/yql?format=json&u=c&d=5&"
    yql_query = "select * from weather.forecast where u='c' and woeid in (select woeid from geo.places(1) " \
                "where text=\"{0}\")"

    def __init__(self, city, period):
        self.city = city
        self.period = period
        self.forecast = None
        self.humidity = None
        self.min = None
        self.max = None
        self.average = None
        self.median = None

    def fetch(self):
        """

        :return:
        """
        query = self.yql_query.format(self.city)
        url = self.baseurl + 'q=' + urllib.quote(query)
        print(url)
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        channel = data['query']['results']['channel']
        return channel

    def compute(self):
        """
        computes and sets this object's max, min, average and median based on yahoo weather data
        median is obtained from a list which aggregates min and max temperature
        """
        channel = self.fetch()
        self.humidity = channel['atmosphere']['humidity']
        forecast = channel['item']['forecast'][:self.period]
        t_max = 0.0
        t_min = float("inf")
        average = 0.0
        all_t = []
        for weather in forecast:
            # sometimes 'high'/'low' is a string...
            weather['high'] = float(weather['high'])
            weather['low'] = float(weather['low'])
            t_max = max(t_max, weather['high'])
            t_min = min(t_min, float(weather['low']))
            average += (weather['high'] + weather['low']) / 2.0
            all_t.append(weather['high'])
            all_t.append(weather['low'])

        self.average = average / len(forecast)
        self.median = median(all_t)
        self.max = t_max
        self.min = t_min

    def __str__(self):
        rep = ("city: {0}\n" +
               "period: {1}\n" +
               "max: {2}\n" +
               "min: {3}\n" +
               "average: {4}\n" +
               "median: {5}\n").format(
            self.city,
            self.period,
            self.max,
            self.min,
            self.average,
            self.median
        )
        return rep

    @property
    def json(self):
        return {
            'city': self.city,
            'period': self.period,
            'max': self.max,
            'min': self.min,
            'average': self.average,
            'median': self.median
        }