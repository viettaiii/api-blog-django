from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import NotificationSerializer
from .models import Notification


class GetNotificationsView(APIView):

    def get(self, request):
        """
            Get list notifications
        Returns:
            - If successful return response 200
        """

        queryset = Notification.objects.all()
        
        res = Response()
        serializer = NotificationSerializer(queryset, many=True)

        res.data = {
            'message': "list notifications",
            'data': serializer.data
        }
        res.status_code = status.HTTP_200_OK
        return res
