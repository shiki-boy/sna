from dj_rest_auth.serializers import PasswordChangeSerializer, JWTSerializer

from rest_framework import serializers

from django.conf import settings
from django.db import transaction
from django.conf import settings

from apps.user.models import User
from apps.util.utils import send_email


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
                  'password', ]

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def save(self, request):
        return super().save()


class SnaLoginSerializer(JWTSerializer):
    info = serializers.SerializerMethodField()

    def get_info(self, obj):
        return obj['user'].info

class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('info', )
        read_only_fields = ('email',)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'email', 'first_name', 'last_name',
                  'phone_number', 'is_active', 'full_name')


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class SnaPasswordChangeSerializer(PasswordChangeSerializer):

    def save(self):
        self.set_password_form.save()
        send_email(
            subject="Reset Password Successfully",
            recipient_email=[self.user.email],
            from_email=settings.DEFAULT_FROM_EMAIL,
            text_template_path="mail/reset_password_confirm.txt",
            html_template_path="mail/reset_password_confirm.html",
            merge_data={"first_name": self.user.first_name})
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)
