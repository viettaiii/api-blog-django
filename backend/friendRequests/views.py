from users.mixins import AuthenticationPermissionMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FriendRequestSerializer, CreateFriendRequestSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import FriendRequest
from django.db.models import Q


class CreateFriendRequestView(AuthenticationPermissionMixin, APIView):
    @swagger_auto_schema(
        request_body=CreateFriendRequestSerializer,
    )
    def post(self, request):
        """
            Create a friend request
        Args:
            from_user_id (int): (Require) id of the user
        Returns:
            - If successful return response 201
            - If failed return response 404
            - If unauthenticated return response 401 or 403
        """
        res = Response()

        # information about friend request
        info = {
            'to_user': request.data.get('to_user_id'),
            'from_user': request.user.id
        }

        # query
        query = Q(to_user_id=info.get('to_user'), from_user_id=info.get('from_user'))

        queryset = FriendRequest.objects.filter(query).first()
        if queryset:
            "Friend request is not found"
            return Response({'message': "You are requested"}, status=status.HTTP_400_BAD_REQUEST)

        # validate data
        serializer = FriendRequestSerializer(data=info)
        if serializer.is_valid(raise_exception=True):
            # If the information is valid then  was created successfully.
            serializer.save()
            res.data = {
                'message': "created friend request successfully!",
                'data': serializer.data
            }
            res.response_code = status.HTTP_201_CREATED
            return res

        # The friend request was failed.
        res.data = {
            'message': "Created failed"
        }
        res.status_code = status.HTTP_400_BAD_REQUEST
        return res


class GetFriendRequestMeView(AuthenticationPermissionMixin, APIView):

    def get(self, request):
        """
            get list friend request

        Returns:
            - If successful return response 201
            - If failed return response 404
            - If unauthenticated return response 401 or 403
        """
        res = Response()

        query = Q(to_user_id=request.user.id, is_accepted=False)
        queryset = FriendRequest.objects.filter(query)
        serializer = FriendRequestSerializer(queryset, many=True)
        res.data = {
            'message': "get all friend requests me",
            'data': serializer.data
        }
        res.status_code = status.HTTP_200_OK
        return res


class AcceptFriendRequestView(AuthenticationPermissionMixin, APIView):

    def put(self, request, pk):
        """
            accept friend request

        Returns:
            - If successful return response 201
            - If failed return response 404
            - If unauthenticated return response 401 or 403
        """

        res = Response()
        query = Q(from_user_id=pk, to_user_id=request.user.id)
        queryset = FriendRequest.objects.filter(query).first()
        if queryset is None:
            return Response({'message': 'Accept failed'}, status.HTTP_400_BAD_REQUEST)

        # Update friend request
        serializer = FriendRequestSerializer(queryset, {'is_accepted': True}, partial=True)
        if serializer.is_valid(raise_exception=True):
            # If the information is valid then  was created successfully.
            serializer.save()
            res.data = {
                'message': "accepted friend request successfully!",
                'data': serializer.data
            }
            res.response_code = status.HTTP_201_CREATED
            return res
        
        # Accept friend request failed!
        res.data = {
            'message': "Accept friend request failed!",
        }
        res.status_code = status.HTTP_400_BAD_REQUEST
        return res


class RejectFriendRequestView(AuthenticationPermissionMixin, APIView):

    def put(self, request, pk):
        """
            reject friend request

        Returns:
            - If successful return response 201
            - If failed return response 404
            - If unauthenticated return response 401 or 403
        """
        res = Response()
        queryset = FriendRequest.objects.filter(from_user=pk).first()
        if queryset is None:
            return Response({'message': "Reject friend request failed!"}, status.HTTP_400_BAD_REQUEST)
        queryset.delete()
        res.data = {
            'message': "reject friend request successfully!",
        }
        res.status_code = status.HTTP_200_OK
        return res


class UnFriendRequestView(AuthenticationPermissionMixin, APIView):

    def put(self, request, pk):
        """
            unfriend friend request

        Returns:
            - If successful return response 201
            - If failed return response 404
            - If unauthenticated return response 401 or 403
        """
        res = Response()
        query = Q(from_user_id=pk, to_user_id=request.user.id, is_accepted=True)
        query.add(Q(to_user_id=pk, from_user_id=request.user.id, is_accepted=True), Q.OR)
        queryset = FriendRequest.objects.filter(query).first()
        if queryset is None:
            return Response({'message': "Reject friend request failed!"}, status.HTTP_400_BAD_REQUEST)
        queryset.delete()
        res.data = {
            'message': "unfriend successfully!",
        }
        res.status_code = status.HTTP_200_OK
        return res


class GetFriendsView(AuthenticationPermissionMixin, APIView):
    def get(self, request):
        """
            get list friends

        Returns:
            - If successful return response 201
            - If failed return response 404
            - If unauthenticated return response 401 or 403
        """
        res = Response()
        query = Q(to_user_id=request.user.id, is_accepted=True)
        query.add(Q(from_user_id=request.user.id, is_accepted=True), Q.OR)
        queryset = FriendRequest.objects.filter(query)
        serializer = FriendRequestSerializer(queryset, many=True)

        res.data = {
            'message': "get all friends",
            'data': serializer.data
        }
        res.status_code = status.HTTP_200_OK
        return res
