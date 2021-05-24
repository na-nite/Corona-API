from django.urls import path

from .views import ReportCase, ListCases, AcceptCases, RejectCases, AddEmails, CCEmailsView

urlpatterns = [
    path('cases/', ListCases.as_view(), name='list-case'),
    path('case/report/', ReportCase.as_view(), name='report-case'),
    path('case/update/accept/<int:pk>', AcceptCases.as_view(), name='accept-case'),
    path('case/update/reject/<int:pk>', RejectCases.as_view(), name='reject-case'),
    path('cc/add/', AddEmails.as_view(), name='add-cc'),
    path('cc/<int:pk>', CCEmailsView.as_view(), name='delete-cc'),
]
