from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer, CreatePostSerializer
from users.mixins import AuthenticationPermissionMixin
from rest_framework.views import APIView
from .models import Post
from users.utils.permission import check_permission
from drf_yasg import openapi
from rest_framework import parsers
from drf_yasg.utils import swagger_auto_schema
from notifications.serializers import NotificationSerializer

from django.db import connection, reset_queries
import time
import functools


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print("Function : " + func.__name__)
        print("Number of Queries : {}".format(end_queries - start_queries))
        print("Finished in : {}".format(end - start))

        return result

    return inner_func


class CreatePostView(AuthenticationPermissionMixin, APIView):
    # parser_classes = (parsers.MultiPartParser,)

    @swagger_auto_schema(
        request_body=CreatePostSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="image",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="Select a file to upload",
                format="binary",  # Set the format to binary for file input
            ),
        ],
    )
    def post(self, request):
        """
            Create a new post
        Args:
            title (str): Title of the post
            content (str): Content of the post
            image (str): Image of the post
            category (str): Category of the post
        Returns:
            - If successful return response 201
            - If failed return response 404
            - If unauthenticated return response 401 or 403
        """
        res = Response()
        # Get user from middleware [AuthenticationPermissionMixin]
        info = {
            'user': request.user.id,
            'title': request.data.get('title'),
            'content': request.data.get('content'),
            'image':  request.data.get('image'),
            'category': request.data.get("category")
        }
        # Check information user input.
        serializer = PostSerializer(data=info)
        if serializer.is_valid(raise_exception=True):
            # If the information is valid then the post was created successfully.
            serializer.save()
            res.data = {
                'message': "Post created successfully!",
                'post': serializer.data
            }

            # Create a new notification
            info_notification = {
                'user': request.user.id,
                'title': request.user.email + ' có một bài đăng mới',
                'content': 'Nội dung so hot',
            }
            serializer_notification = NotificationSerializer(data=info_notification)
            if serializer_notification.is_valid(raise_exception=True):
                serializer_notification.save()

            # return
            res.status_code = status.HTTP_201_CREATED
            return res

        # The post was failed when created.
        res.data = {
            'message': "Created failed"
        }
        res.status_code = status.HTTP_400_BAD_REQUEST
        return res


CATEGORY_CHOICES = [
    ('fashion', 'Fashion'),
    ('beauty', 'Beauty'),
    ('travel', 'Travel'),
    ('lifestyle', 'Lifestyle'),
    ('personal', 'Personal'),
    ('tech', 'Tech'),
    ('health', 'Health'),
    ('fitness', 'Fitness'),
    ('wellness', 'Wellness'),
]


class GetAllPostView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Pagination parameter", type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Limit parameter", type=openapi.TYPE_INTEGER),
            openapi.Parameter('sort', openapi.IN_QUERY, description="Sort parameter", type=openapi.TYPE_STRING),
            openapi.Parameter('category', openapi.IN_QUERY, description="Category parameter", type=openapi.TYPE_STRING, enum=[
                              'fashion', 'beauty', 'travel', 'lifestyle', 'personal', 'tech', 'health', 'fitness', 'wellness']),
        ],
    )
    @query_debugger
    def get(self, request):
        """
            Get all posts
        Returns:
            Post : return list posts
        """
        res = Response()

        # Pagination
        limit = int(request.GET.get("limit", 4))
        page = int(request.GET.get('page', 1))
        offset = (page - 1) * limit
        category = request.GET.get("category", None)

        # sorting
        sort = request.GET.get('sort', '-created_at')
        queryset = None

        # filter category
        if category:
            queryset = Post.objects.select_related('user').filter(category=category)
        else:
            queryset = Post.objects.select_related('user').all()
        # queryset = queryset.order_by(sort)[(offset):(offset + limit)]

        # count records
        # total_records = Post.objects.count()

        # Check information user input.
        serializer = PostSerializer(queryset, many=True)
        posts = []
        for post in queryset:
            posts.append({
                'id': post.id,
                'user': post.user.email,
                'title': post.title,
                'content': post.content
            })

        # queryset = Post.objects.select_related('user').all()
        # posts = []
        # for post in queryset:
        #     posts.append({
        #         'id': post.id,
        #         'user': post.user.email
        #     })
        res.data = {
            'message': "List posts",
            'page': page,
            'limit': limit,
            # 'total_records': total_records,
            'data': posts
        }

        res.status_code = status.HTTP_200_OK
        return res


class GetAllPostMeView(AuthenticationPermissionMixin, APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Pagination parameter", type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Limit parameter", type=openapi.TYPE_INTEGER),
            openapi.Parameter('sort', openapi.IN_QUERY, description="Sort parameter", type=openapi.TYPE_STRING),
            openapi.Parameter('category', openapi.IN_QUERY, description="Category parameter", type=openapi.TYPE_STRING, enum=[
                              'fashion', 'beauty', 'travel', 'lifestyle', 'personal', 'tech', 'health', 'fitness', 'wellness']),
        ],
    )
    def get(self, request):
        """
            Get all posts me
        Returns:
            Post : return list posts
        """

        res = Response()

        # Pagination
        limit = int(request.GET.get("limit", 4))
        page = int(request.GET.get('page', 1))
        offset = (page - 1) * limit
        category = request.GET.get("category", None)

        # sorting
        sort = request.GET.get('sort', '-created_at')
        queryset = None

        queryset = Post.objects.filter(user_id=request.user.id)
        # filter category
        if category:
            queryset = Post.objects.filter(category=category)

        queryset = queryset.order_by(sort)[(offset):(offset + limit)]

        # count records
        total_records = Post.objects.count()

        serializer = PostSerializer(queryset, many=True)
        res.data = {
            'message': "List posts",
            'page': page,
            'limit': limit,
            'total_records': total_records,
            'data': serializer.data
        }
        res.status_code = status.HTTP_200_OK
        return res


class UpdatePostView(AuthenticationPermissionMixin, APIView):
    @swagger_auto_schema(
        request_body=CreatePostSerializer
    )
    def put(self, request, pk):
        """
            Update a post
        args:
            pk (int): The id of the post to update.
            content (str): Optional content of the post.
            image (str): Optional image of the post.
        Returns:
            - If successful response status code 200
            - If Authenticated response status code 401
            - If Permission denied response status code 403 
            - If Information is not valid response status 404
        """
        res = Response()

        # Get information post by id
        post = get_object_or_404(Post, pk=pk)

        # Check permission
        check_permission(request.user.id, post.user_id)

        # Validation data
        serializer = PostSerializer(post, data=request.data, partial=True)
        if not serializer.is_valid(raise_exception=True):
            # If have a error then return error
            pass
        serializer.save()

        # Update post successfully
        res.data = {
            'message': "Update post successfully",
            'data': serializer.data
        }
        res.status_code = status.HTTP_200_OK
        return res


class DeletePostView(AuthenticationPermissionMixin, APIView):
    def delete(self, request, pk):
        """
            Delete a post
        args:
            pk (int): The id of the post to delete.
        Returns:
            - If successful response status code 200
            - If Authenticated response status code 401
            - If Permission denied response status code 403 
        """
        res = Response()

        # Get information post by id
        post = get_object_or_404(Post, pk=pk)

        # Check permission if permission denied then return error
        check_permission(request.user.id, post.user_id)

        # Delete post successfully
        post.delete()
        res.data = {
            'message': "Delete post successfully",
        }
        res.status_code = status.HTTP_200_OK
        return res


class GetDetailPostView(APIView):
    def get(self, request, pk):
        """
            Get detail a post
        args:
            pk (int): The id of the post to get.
        Returns:
            - If successful response status code 200
            - If post isn`t existing then response status code 404
        """
        res = Response()

        # Get information post by id
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, many=False)

        # get a post successfully
        res.data = {
            'message': "get a post successfully",
            'data': serializer.data
        }
        res.status_code = status.HTTP_200_OK
        return res
