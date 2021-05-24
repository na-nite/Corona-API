from django.urls import path
from api_diagnostic.views import DiagnoseCreate, Answer

urlpatterns = [
    path('answer/', Answer.as_view(), name='answer'),
    path('diagnose/', DiagnoseCreate.as_view(), name='diagnose'),
    #path('answermoderator/', AnswerModerator.as_view(), name='answerModerator'),


]
