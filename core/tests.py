from django.test import TestCase

from core import median, Weather


class CoreTests(TestCase):

    def test_utils_median(self):
        l = [1, 2, 3, 4, 5, 6, 7]
        self.assertEquals(median(l), 4)

        l = [1, 2, 3, 4, 5, 6, 7, 8]
        self.assertEquals(median(l), (4+5)/2.0)

    def test_weather(self):
        old_fetch = Weather.fetch

        def test_fetch(self):
            return {
                'atmosphere': {'humidity': 34},
                'item': {
                    'forecast': [{
                        'high': 20,
                        'low': 10
                    }, {
                        'high': 30,
                        'low': 10
                    }, {
                        'high': 40,
                        'low': 20
                    }]
                }
            }
        Weather.fetch = test_fetch

        w = Weather(city='london', period=10)
        w.compute()

        self.assertEquals(w.min, 10)
        self.assertEquals(w.max, 40)
        self.assertEquals(w.average, (20+10+40+20+30+10) / 6.0)
        self.assertEquals(w.median, 20) # 10 10 (20 20) 30 40
        self.assertEquals(w.humidity, 34)

        w.period = 2
        w.compute()
        self.assertEquals(w.average, (20+10+30+10) / 4.0)
        self.assertEquals(w.median, 15) # 10 10 20 30
        self.assertEquals(w.max, 30)

        Weather.fetch = old_fetch

    def test_weather_api(self):
        w = Weather(city='london', period=10)
        w.compute()
        self.assertTrue(w.min is not None)
        self.assertTrue(w.max is not None)
        self.assertTrue(w.average is not None)
        self.assertTrue(w.median is not None)
        self.assertTrue(w.humidity is not None)