from django.contrib.auth.models import User
from django.db import models
from bs4 import BeautifulSoup
import urllib.request
from app import settings


class RobotYoutube(models.Model):
    title = models.CharField(max_length=255)
    vedio = models.CharField(max_length=255)
    thumb = models.CharField(max_length=255)
    Status_CHOICES = (
        (1, 'pending'),
        (2, 'accepted'),
        (3, 'rejected'),
    )
    status = models.PositiveSmallIntegerField(choices=Status_CHOICES, default=1)

    def youtube_get_vedios(textToSearch):
        vedios = []
        query = urllib.parse.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        vids = soup.findAll(attrs={'class': 'yt-uix-tile-link'})
        i = 0
        for vid in vids:
            if not vid['href'].startswith("https://googleads.g.doubleclick.net/"):
                vedios.append(
                    {'title': vid['title'],
                     'link': 'https://www.youtube.com' + vid['href'],
                     'img': vid.parent.parent.parent.find('img')['src']})
                i += 1
                if i == 6:
                    return vedios
        return vedios
