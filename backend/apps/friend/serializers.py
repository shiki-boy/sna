from rest_framework import serializers

from django.db.models import Q

from apps.user.models import User
from apps.util.serializers import UIDField

from .models import Friendship


class FriendshipSerializer(serializers.ModelSerializer):
    status_label = serializers.ReadOnlyField(source="get_status_display")
    friend_a = UIDField(model=User, field="full_name")
    friend_r = UIDField(model=User, field="full_name", required=False)

    class Meta:
        model = Friendship
        fields = ("uid", "status_label", "friend_r", "friend_a", "created")

    def create(self, validated_data):
        # checking if already exists or not
        if Friendship.objects.filter(
            Q(friend_r=validated_data["friend_r"], friend_a=validated_data["friend_a"])
            | Q(
                friend_a=validated_data["friend_r"], friend_r=validated_data["friend_a"]
            )
        ).exists():
            raise serializers.ValidationError(
                detail={"message": "This request already exists"}
            )
        return super().create(validated_data)


class SearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("uid", "first_name", "last_name")


class ListFriendsSerializer(serializers.ModelSerializer):
    friend_a = UIDField(model=User)
    friend_a_name = serializers.ReadOnlyField(source="friend_a.full_name")
    friend_r = UIDField(model=User)
    friend_r_name = serializers.ReadOnlyField(source="friend_r.full_name")

    class Meta:
        model = Friendship
        fields = ("uid", "friend_r", "friend_r_name", "friend_a", "friend_a_name")
