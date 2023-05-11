from rest_framework.routers import DefaultRouter

from django.urls import path

from .views import FriendshipViewset, SearchAPIView, ListFriendsAPIView

router = DefaultRouter()

router.register("request", FriendshipViewset)

urlpatterns = [
    path('list/', ListFriendsAPIView.as_view(), name='search-api'),
    path('search/', SearchAPIView.as_view(), name='search-api'),
]

urlpatterns += router.urls
