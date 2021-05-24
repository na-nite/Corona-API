from django.urls import path

from api_map.views import NationalZoneList, NationalZoneListId, NationalZoneRetrieveUpdate, \
    NationalZoneStatusUpdate, NationalZoneCreate, InternationalZoneStatusUpdate, InternationalZoneRetrieveUpdate, \
    InternationalZoneCreate, InternationalZoneListId, InternationalZoneList, Wilayas, Communes

urlpatterns = [
    path('national-zone/', NationalZoneList.as_view(), name='list-national-zone'),
    path('national-zone/<int:pk>/', NationalZoneListId.as_view(), name='list-national-zone-id'),
    path('national-zone/create/', NationalZoneCreate.as_view(), name='create-zone'),
    path('national-zone/update/<int:pk>/', NationalZoneRetrieveUpdate.as_view(), name='update-zone-info'),
    path('national-zone/update-status/<int:pk>/', NationalZoneStatusUpdate.as_view(), name='update-status-zone'),

    path('international-zone/', InternationalZoneList.as_view(), name='list-international-zone'),
    path('international-zone/<int:pk>/', InternationalZoneListId.as_view(), name='list-international-zone-id'),
    path('international-zone/create/', InternationalZoneCreate.as_view(), name='create-zone'),
    path('international-zone/update/<int:pk>/', InternationalZoneRetrieveUpdate.as_view(), name='update-zone-info'),
    path('international-zone/update-status/<int:pk>/', InternationalZoneStatusUpdate.as_view(),
         name='update-status-zone'),

    path('wilaya/', Wilayas.as_view(), name='wilayas'),
    path('communes/', Communes.as_view(), name='communes'),
]
