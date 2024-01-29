from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LikeCommentSerializer, CreateLikeCommentSerializer
from .models import LikeComment
# Create your views here.
from users.mixins import AuthenticationPermissionMixin
from comments.models import Comment
from users.utils.permission import check_permission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CreateLikeCommentView(AuthenticationPermissionMixin, APIView):
    @swagger_auto_schema(
        request_body=CreateLikeCommentSerializer,
    )
    def post(self, request):
        """
            Create a new like
        Args:
            user_id (int): (Require) id of the user
            comment_id (int): (Require)id of the comment
        Returns:
            - If successful return response 201
            - If failed return response 404
            - If unauthenticated return response 401 or 403
        """
        res = Response()

        # Get user from middleware [AuthenticationPermissionMixin]

        # Check post by id
        comment = get_object_or_404(Comment, pk=request.data.get('comment_id'))

        # information about new comment
        info = {
            'comment': comment.id,
            'user': request.user.id
        }

        serializer = LikeCommentSerializer(data=info)
        if serializer.is_valid(raise_exception=True):
            # If the information is valid then  was created successfully.
            serializer.save()
            res.data = {
                'message': "like created successfully!",
                'data': serializer.data
            }
            res.response_code = status.HTTP_201_CREATED
            return res

        # The comment was failed.
        res.data = {
            'message': "Created failed"
        }
        res.status_code = status.HTTP_400_BAD_REQUEST
        return res


class DeleteLikeCommentView(AuthenticationPermissionMixin, APIView):
    def delete(self, request, pk):
        """
            delete a like comment
        Args:
            pk (int): (Require) id of the like
        Returns:
            - If successful return response 200
            - If unauthenticated return response 401 or 403
        """
        res = Response()

        like = get_object_or_404(LikeComment, pk=pk)

        # check permission
        check_permission(request.user.id, like.user_id)

        like.delete()
        # deleted successfully
        res.data = {
            'message': "deleted successfully"
        }
        res.status_code = status.HTTP_200_OK
        return res


class GetAllLikeCommentView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('sort', openapi.IN_QUERY, description="Sort parameter", type=openapi.TYPE_STRING),
            openapi.Parameter('comment_id', openapi.IN_QUERY, description="comment parameter", type=openapi.TYPE_STRING),
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
        comment_id = request.GET.get("comment_id", None)
        user_id = request.GET.get("user_id", None)

        # sorting
        sort = request.GET.get('sort', '-created_at')
        queryset = None

        queryset = LikeComment.objects.all()
        if comment_id:
            queryset = queryset.filter(comment_id=comment_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        queryset = queryset.order_by(sort)
        res = Response()
        serializer = LikeCommentSerializer(queryset, many=True)

        res.data = {
            'message': "Get all likes comment",
            'data': serializer.data
        }
        res.status_code = status.HTTP_200_OK
        return res
