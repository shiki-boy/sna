from rest_framework.routers import DefaultRouter

from django.urls import path

from .views import FriendshipViewset, SearchAPIView

router = DefaultRouter()

router.register("request", FriendshipViewset)

urlpatterns = [
    path('search/', SearchAPIView.as_view(), name='search-api'),
]

urlpatterns += router.urls
