from django.urls import path

from api_robot.views import YoutubeVediosCreate, YoutubeVedios, YoutubeVediosAccept, YoutubeVediosReject

urlpatterns = [
    path('youtube-vedios-create/', YoutubeVediosCreate.as_view(), name='vedio-create'),
    path('youtube-vedios-list/', YoutubeVedios.as_view(), name='vedio-list'),
    path('youtube-vedios-accept/<int:pk>', YoutubeVediosAccept.as_view(), name='vedio-accepted'),
    path('youtube-vedios-reject/<int:pk>', YoutubeVediosReject.as_view(), name='vedio-rejected'),

]
