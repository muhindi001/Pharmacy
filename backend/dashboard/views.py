from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DashboardSerializer
from .services import DashboardService


class DashboardAPIView(APIView):

    def get(self, request):

        data = DashboardService.get_dashboard()

        serializer = DashboardSerializer(data)

        return Response(serializer.data)