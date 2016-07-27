from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class WeatherAPITests(APITestCase):

    def test_main_entry_point(self):
        url = reverse('weather')
        response = self.client.get(url, {'city': 'london', 'period': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.data
        self.assertTrue('data' in content)
        self.assertTrue('city' in content['data'])
        self.assertTrue('min' in content['data'])
        self.assertTrue('max' in content['data'])
        self.assertTrue('average' in content['data'])
        self.assertTrue('median' in content['data'])
