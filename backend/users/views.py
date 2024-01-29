from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserLoginSerializer
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from rest_framework import exceptions
import jwt
from .mixins import AuthenticationPermissionMixin
from drf_yasg.utils import swagger_auto_schema


class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
    )
    def post(self, request):
        """
            Register a new user
        Args:
            email (str): The email address
            password (str): The password 

        Returns:
            - If the register is successful then response User and status 201
            - If the register is failed then response status 404
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # hash password
            validated_data = serializer.validated_data
            password = make_password(validated_data.get('password'))
            validated_data['password'] = password
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
    )
    def post(self, request):
        """
            Login a new user
        Args:
            email (str): The email address 
            password (str): The password 

        Returns:
            - If the register is successful then response User and status 201
            - If the register is failed then response status 404
        """

        # find a user by email
        user = User.objects.filter(email=request.data.get('email')).first()

        # check user is existing
        if user is None:
            raise exceptions.NotFound("User not found!")

        # check password
        is_checked_password = check_password(request.data.get('password'), user.password)
        if not is_checked_password:
            raise exceptions.AuthenticationFailed("Password is incorrect!")

        # create token and refresh token
        serializer = UserSerializer(user, many=False)
        payload = {
            'id': serializer.data.get('id'),
            'email': serializer.data.get('email'),
        }
        token = jwt.encode(payload, "secret", algorithm="HS256")

        res = Response()
        res.set_cookie(key='access_token', value=token, httponly=True)
        res.data = {
            "access_token": token,
        }
        res.status_code = status.HTTP_200_OK
        return res


class GetMeView(
    AuthenticationPermissionMixin,  # Middleware get user by token on cookie
    APIView
):
    """
        Get user is logged in
    """

    def get(self, request):
        serializer = UserSerializer(request.user, many=False)
        # response
        res = Response()

        res.data = serializer.data
        return res


class LogoutView(
    AuthenticationPermissionMixin,  # Middleware get user by token on cookie
    APIView
):
    """
        Logout user
    """

    def post(self, request):

        res = Response()
        res.delete_cookie('access_token')
        res.data = {
            'message': "Logged in successfully"
        }
        return res
# class BlockUserView(APIView):
#     def put(self, request, pk):
#         """
#             Block a user
#         Returns:
#             - If the register is successful then response User and status 201
#             - If the register is failed then response status 404
#         """

#         # find a user by email
#         user = User.objects.filter(pk=pk).first()

#         # check user is existing
#         if user is None:
#             raise exceptions.NotFound("User not found!")

#         # update user is_block
#         user.is_blocked = True
#         serializer = UserSerializer(user, many=False)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()

#         res = Response()
#         res.data = {
#             "message": "Blocked successfully!",
#         }
#         res.status_code = status.HTTP_200_OK
#         return res


class GetAllUserView(APIView):
    def get(self, request):
        """
            Get list user
        Returns:
            - If successful return response 200
        """
        res = Response()
        queryset = User.objects.all()

        serializer = UserSerializer(queryset, many=True)

        res.data = {
            'message': "Get list user",
            'data': serializer.data
        }
        res.status_code = status.HTTP_200_OK
        return res
