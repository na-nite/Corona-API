from django.http import JsonResponse, HttpResponse
from django.conf import settings

from rest_framework.permissions import AllowAny
from requests.exceptions import HTTPError

from rest_framework.permissions import (IsAuthenticated, IsAdminUser)
from rest_framework.response import Response
from rest_framework.decorators import api_view, \
    permission_classes, authentication_classes
from django.contrib.auth import login as django_login, \
    logout as django_logout
from .serializers import (RegistrationSerializer,
                          LoginVisitorSerializer, UserSerializer,
                          LoginStaffSerializer, AddUserSerializer,
                          DeleteUserSerializer, SocialSerializer)
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from user.models import User
from rest_framework import status, generics
from social_django.utils import psa


@api_view(['POST', ])
def registration_view(request):
    """
serializer: api_content.UserSerializer
parameters_strategy:
    form: replace
parameters:
    - name: email
      type: String
      required: true
      paramType: form
    """
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['email'] = user.email
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
            data['birth_date'] = user.birth_date
        else:
            data = serializer.errors
        return JsonResponse(data)


@api_view(['POST', ])
def login_visitor_view(request):
    serializer = LoginVisitorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    django_login(request, user)
    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=200)


@api_view(['POST', ])
def login_staff_view(request):
    serializer = LoginStaffSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    django_login(request, user)
    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=200)


@api_view(['POST', ])
@authentication_classes(['TokenAuthentication',
                         'SessionAuthentication'])
def logout_view(request):
    django_logout(request)
    return Response(status=204)


@api_view(['GET', ])
# admin permission and moderator permission only
def user_listing_view(request):
    """list all the users"""
    data = User.objects.all()
    serializer = UserSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
def user_detail_view(request, pk):
    """list the user who has the id = pk"""
    data = User.objects.get(pk=pk)
    serializer = UserSerializer(data)
    return Response(serializer.data)


@api_view(['GET', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def add_user_view(request):
    if request.user.is_superuser:
        serializer = AddUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'msg': 'user created successfully'
            }
        else:
            data = serializer.errors
        return JsonResponse(data, status=200)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UpdateUSer(generics.RetrieveUpdateAPIView):
    """
    Update post
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class DeleteUser(generics.DestroyAPIView):
    """
    delete user
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = DeleteUserSerializer
    queryset = User.objects.all()


class BlockUser(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = DeleteUserSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        serializer.save(is_active=False)


class UnblockUser(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = DeleteUserSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        serializer.save(is_active=True)


@api_view(['POST'])
@psa()
def exchange_token(request, backend):
    """
    Exchange an OAuth2 access token for one for this site.
    This simply defers the entire OAuth2 process to the front end.
    The front end becomes responsible for handling the entirety of the
    OAuth2 process; we just step in at the end and use the access token
    to populate some user identity.
    The URL at which this view lives must include a backend field, like:
        url(API_ROOT + r'social/(?P<backend>[^/]+)/$', exchange_token),
    Using that example, you could call this endpoint using i.e.
        POST API_ROOT + 'social/facebook/'
        POST API_ROOT + 'social/google-oauth2/'
    Note that those endpoint examples are verbatim according to the
    PSA backends which we configured in settings.py. If you wish to enable
    other social authentication backends, they'll get their own endpoints
    automatically according to PSA.
    ## Request format
    Requests must include the following field
    - `access_token`: The OAuth2 access token provided by the provider
    """
    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = 'non_field_errors'

        try:
            user = request.backend.do_auth(serializer.validated_data['access_token'])
        except HTTPError as e:
            return Response(
                {'errors': {
                    'token': 'Invalid token',
                    'detail': str(e),
                }},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            if user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response(
                    {'errors': {nfe: 'This user account is inactive'}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:

            return Response(
                {'errors': {nfe: "Authentication Failed"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
