from rest_framework.views import APIView
from rest_framework.response import Response
from core import Weather


class WeatherView(APIView):

    def get(self, request, format=None):
        """
        :param request: Request
        :param city: str
        """
        city = request.GET['city']
        period = int(request.GET['period'])
        w = Weather(city=city, period=period)
        w.compute()
        return Response({'data': w.json})