from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter

from django.db.models import Q

from apps.user.models import User

from .serializers import FriendshipSerializer, SearchUserSerializer
from .models import Friendship


# list, create, delete, actions -> acceptordeny
class FriendshipViewset(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet
):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendshipSerializer
    queryset = Friendship.objects.all()
    lookup_field = "uid"
    lookup_url_kwarg = "uid"
    lookup_value_regex = "[0-9a-f-]{36}"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(status=Friendship.STATUS_CHOICES.PENDING)
            .filter(Q(friend_r=self.request.user) | Q(friend_a=self.request.user))
        )

    def perform_create(self, serializer):
        serializer.save(friend_r=self.request.user)    

    def destroy(self, request, *args, **kwargs):
        if self.get_object().friend_r != self.request.user:
            return Response({"message": "You cannot delete this request"}, 403)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["PUT"], url_path="update", url_name="update_status")
    def update_status(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.friend_a != self.request.user:
            return Response({"message": "You cannot update this request"}, 403)

        status = self.request.query_params.get("status", None)

        if (
            not status
            or status not in Friendship.STATUS_CHOICES.values
            or status == Friendship.STATUS_CHOICES.PENDING
        ):
            return Response({"message": "Invalid request"}, 400)

        obj.status = status
        obj.save()
        return Response({"message": "Status changed successfully"})


class SearchAPIView(ListAPIView):
    serializer_class = SearchUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    ordering = ["first_name"]
    search_fields = ["first_name", "last_name", "=email"]

    def get_queryset(self):
        return User.objects.exclude(is_superuser=True).exclude(is_staff=True)
