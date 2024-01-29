from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LikePostSerializer, CreateLikePostSerializer

# Create your views here.
from users.mixins import AuthenticationPermissionMixin
from .models import LikePost
from posts.models import Post
from users.utils.permission import check_permission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CreateLikeView(AuthenticationPermissionMixin, APIView):
    @swagger_auto_schema(
        request_body=CreateLikePostSerializer,
    )
    def post(self, request):
        """
            Create a new like
        Args:
            user_id (int): (Require) id of the user
            post_id (int): (Require)id of the post
        Returns:
            - If successful return response 201
            - If failed return response 404
            - If unauthenticated return response 401 or 403
        """
        res = Response()

        # Check post by id
        post = get_object_or_404(Post, pk=request.data.get('post_id'))

        # information
        info = {
            'post': post.id,
            'user': request.user.id
        }

        serializer = LikePostSerializer(data=info)
        if serializer.is_valid(raise_exception=True):
            # If the information is valid then  was created successfully.
            serializer.save()
            res.data = {
                'message': "like created successfully!",
                'data': serializer.data
            }
            res.response_code = status.HTTP_201_CREATED
            return res

        # The like was failed.
        res.data = {
            'message': "Created like failed"
        }
        res.status_code = status.HTTP_400_BAD_REQUEST
        return res


class DeleteLikeView(AuthenticationPermissionMixin, APIView):
    def delete(self, request, pk):
        """
            delete a like
        Args:
            pk (int): (Require) id of the like
        Returns:
            - If successful return response 200
            - If unauthenticated return response 401 or 403
        """
        res = Response()

        like = get_object_or_404(LikePost, pk=pk)

        # check permission
        check_permission(request.user.id, like.user_id)

        like.delete()
        # deleted successfully
        res.data = {
            'message': "deleted successfully"
        }
        res.status_code = status.HTTP_200_OK
        return res


class GetAllLikeView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('sort', openapi.IN_QUERY, description="Sort parameter", type=openapi.TYPE_STRING),
            openapi.Parameter('post_id', openapi.IN_QUERY, description="post parameter", type=openapi.TYPE_STRING),
            openapi.Parameter('user_id', openapi.IN_QUERY, description="user parameter", type=openapi.TYPE_STRING),
        ],
    )
    def get(self, request):
        """
            Get list likes
        Returns:
            - If successful return response 200
        """

        # Pagination
        limit = int(request.GET.get("limit", 4))
        page = int(request.GET.get('page', 1))
        offset = (page - 1) * limit
        post_id = request.GET.get("post_id", None)
        user_id = request.GET.get("user_id", None)

        # sorting
        sort = request.GET.get('sort', '-created_at')
        queryset = None

        queryset = LikePost.objects.all()
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        queryset = queryset.order_by(sort)
        res = Response()
        serializer = LikePostSerializer(queryset, many=True)

        res.data = {
            'message': "Get all likes",
            'data': serializer.data
        }
        res.status_code = status.HTTP_200_OK
        return res
