from django.contrib import admin
from notification.models import Notification, CCEmails

admin.site.register(Notification)
admin.site.register(CCEmails)
