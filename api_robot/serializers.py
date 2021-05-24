import urllib

from bs4 import BeautifulSoup
from rest_framework import serializers

from SuspectedCase.models import SuspectedCase
from notification.models import CCEmails
from robot.models import RobotYoutube

SC_FIELD = [
    'pk',
    'title',
    'vedio',
    'thumb',
    'status',
]

class RobotSerializerStatus(serializers.ModelSerializer):
    class Meta:
        model = RobotYoutube
        fields = SC_FIELD
        read_only_fields = ('title', 'vedio', 'thumb')

class RobotYoutubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobotYoutube
        fields = SC_FIELD
        read_only_fields = ('title', 'vedio', 'thumb', 'status')


class RobotYoutubeFullSerializer(serializers.ModelSerializer):
    search_query = serializers.CharField(required=True, )

    class Meta:
        model = RobotYoutube
        fields = SC_FIELD + ['search_query', ]
        read_only_fields = ('title', 'vedio', 'thumb', 'status',)
        extra_kwargs = {'search_query': {'write_only': False}}

    def save(self):
        search_query = self.validated_data['search_query']
        query = urllib.parse.quote(search_query)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        vids = soup.findAll(attrs={'class': 'yt-uix-tile-link'})
        i = 0
        for vid in vids:
            if not vid['href'].startswith("https://googleads.g.doubleclick.net/"):
                ved = RobotYoutube(
                    title=vid['title'],
                    vedio='https://www.youtube.com' + vid['href'],
                    thumb=vid.parent.parent.parent.find('img')['src'],
                    status=1,
                )
                ved.save()
                i += 1
                if i == 6:
                    break
