from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CommentSerializer, CreateCommentSerializer, ReplyCommentSerializer, UpdateCommentSerializer
from users.serializers import UserSerializer
# Create your views here.
from users.mixins import AuthenticationPermissionMixin
from .models import Comment
from posts.models import Post
from posts.serializers import PostSerializer
from users.utils.permission import check_permission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CreateCommentView(AuthenticationPermissionMixin, APIView):
    @swagger_auto_schema(
        request_body=CreateCommentSerializer,
    )
    def post(self, request):
        """
            Create a new comment
        Args:
            content (str): (Optional) Content of the comment
            post_id (int): (Require)id of the post
        Returns:
            - If successful return response 201
            - If failed return response 404
            - If unauthenticated return response 401 or 403
        """
        res = Response()

        # Get user from middleware [AuthenticationPermissionMixin]
        user = UserSerializer(request.user, many=False)
        # Check post by id
        post = get_object_or_404(Post, pk=request.data.get('post_id'))
        post_serializer = PostSerializer(post, many=False)
        # Check information comment user input.
        info = {
            'content': request.data.get('content', None),
            'post': post_serializer.data.get('id'),
            'user': user.data.get('id'),
        }

        serializer = CommentSerializer(data=info)
        if serializer.is_valid(raise_exception=True):
            # If the information is valid then the post was created successfully.
            serializer.save()
            res.data = {
                'message': "Comment created successfully!",
                'post': serializer.data
            }
            res.response_code = status.HTTP_201_CREATED
            return res

        # The comment was failed when created.
        res.data = {
            'message': "Created failed"
        }
        res.status_code = status.HTTP_400_BAD_REQUEST
        return res


class ReplyCommentView(AuthenticationPermissionMixin, APIView):
    @swagger_auto_schema(
        request_body=ReplyCommentSerializer,
    )
    def post(self, request):
        """
            Reply a comment
        Args:
            content (str): (Optional) Content of the comment
            comment_id (int): (Require)id of the comment
        Returns:
            - If successful return response 201
            - If failed return response 404
            - If unauthenticated return response 401 or 403
        """
        res = Response()

        # Get user from middleware [AuthenticationPermissionMixin]
        user = UserSerializer(request.user, many=False)

        comment = get_object_or_404(Comment, pk=request.data.get('comment_id'))

        info = {
            'content': request.data.get('content'),
            'parent': comment.id,
            'post': comment.post_id,
            'user': user.data.get('id')
        }

        serializer = CommentSerializer(data=info)
        if serializer.is_valid(raise_exception=True):
            # If the information is valid then the post was created successfully.
            serializer.save()
            res.data = {
                'message': "Reply Comment successfully!",
                'data': serializer.data
            }
            res.response_code = status.HTTP_201_CREATED
            return res

        # The comment was reply when created.
        res.data = {
            'message': "reply failed"
        }
        res.status_code = status.HTTP_400_BAD_REQUEST
        return res


class UpdateCommentView(AuthenticationPermissionMixin, APIView):
    @swagger_auto_schema(
        request_body=UpdateCommentSerializer,
    )
    def put(self, request, pk):
        """
            Update a comment
        Args:
            content (str):  Content of the comment
            pk (int): (Require) id of the comment
        Returns:
            - If successful return response 200
            - If failed return response 404
            - If unauthenticated return response 401 or 403
        """
        res = Response()

        comment = get_object_or_404(Comment, pk=pk)

        # Get user from middleware [AuthenticationPermissionMixin]
        user = UserSerializer(request.user, many=False)
        check_permission(user.data.get('id'), comment.user_id)

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            # If the information is valid then the comment was updated successfully.
            serializer.save()
            res.data = {
                'message': "Comment updated successfully!",
                'data': serializer.data
            }
            res.response_code = status.HTTP_200_OK
            return res

        # The comment was failed when update.
        res.data = {
            'message': "updated failed"
        }
        res.status_code = status.HTTP_400_BAD_REQUEST
        return res


class DeleteCommentView(AuthenticationPermissionMixin, APIView):
    def delete(self, request, pk):
        """
            delete a comment
        Args:
            pk (int): (Require) id of the comment
        Returns:
            - If successful return response 200
            - If unauthenticated return response 401 or 403
        """
        res = Response()

        comment = get_object_or_404(Comment, pk=pk)

        # Get user from middleware [AuthenticationPermissionMixin]
        user = UserSerializer(request.user, many=False)

        # check permission
        check_permission(user.data.get('id'), comment.user_id)

        comment.delete()
        # deleted successfully
        res.data = {
            'message': "deleted successfully"
        }
        res.status_code = status.HTTP_200_OK
        return res


class GetAllCommentView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Pagination parameter", type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Limit parameter", type=openapi.TYPE_INTEGER),
            openapi.Parameter('sort', openapi.IN_QUERY, description="Sort parameter", type=openapi.TYPE_STRING),
            openapi.Parameter('post_id', openapi.IN_QUERY, description="Post parameter", type=openapi.TYPE_STRING),
        ],
    )
    def get(self, request):
        """
            Get list comment
        Returns:
            - If successful return response 200
        """
        # Pagination
        limit = int(request.GET.get("limit", 4))
        page = int(request.GET.get('page', 1))
        offset = (page - 1) * limit
        post_id = request.GET.get('post_id')
        # sorting
        sort = request.GET.get('sort', '-created_at')
        queryset = None
        res = Response()

        if post_id:
            queryset = Comment.objects.filter(post_id=post_id)
        else:
            queryset = Comment.objects.all()
        queryset = queryset.order_by(sort)[(offset):(offset + limit)]
        serializer = CommentSerializer(queryset, many=True)
        total_records = Comment.objects.count()
        # The comment was failed when update.
        res.data = {
            'message': "Get all comments",
            'page': page,
            'limit': limit,
            'total_records': total_records,
            'data': serializer.data
        }
        res.status_code = status.HTTP_200_OK
        return res
