from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, exceptions
from rest_framework.permissions import IsAuthenticated

from api_robot.serializers import RobotYoutubeSerializer, RobotYoutubeFullSerializer, RobotSerializerStatus
from robot.models import RobotYoutube

FILTER_FIELDS = ['status']


class YoutubeVedios(generics.ListAPIView, ):
    """
list youtube vedios
    """
    serializer_class = RobotYoutubeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = FILTER_FIELDS

    def get_queryset(self):
        if not self.request.user.is_staff:
            qs = RobotYoutube.objects.all().filter(status=2)
        else:
            qs = RobotYoutube.objects.all()
        return qs


class YoutubeVediosCreate(generics.CreateAPIView):
    """
        Create youtube content
    """
    serializer_class = RobotYoutubeFullSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', ]

    def get_queryset(self):
        return RobotYoutube.objects.all()


class YoutubeVediosAccept(generics.RetrieveUpdateAPIView):
    """
    A moderator accept a video
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RobotSerializerStatus
    queryset = RobotYoutube.objects.all()

    def get_querset(self):
        if self.request.user.role == 2:
            return RobotYoutube.objects.all()
        else:
            raise exceptions.ValidationError("this user is not allowed to validate posts")

    def perform_update(self, serializer):
        serializer.save(status=2)


class YoutubeVediosReject(generics.RetrieveUpdateAPIView):
    """
    A moderator reject a viedo
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RobotSerializerStatus
    queryset = RobotYoutube.objects.all()

    def get_querset(self):
        if self.request.user.role == 2:
            return RobotYoutube.objects.all()
        else:
            raise exceptions.ValidationError("this user is not allowed to validate posts")

    def perform_update(self, serializer):
        serializer.save(status=3)
