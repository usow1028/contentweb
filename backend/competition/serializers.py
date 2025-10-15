from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Submission, Vote

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'team', 'points']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'team']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Passwords didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class SubmissionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    votes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id',
            'author',
            'title',
            'description',
            'category',
            'content_text',
            'content_file',
            'true_identity',
            'created_at',
            'votes_count',
        ]
        read_only_fields = ['true_identity']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and not request.user.is_staff and request.user != instance.author:
            data.pop('true_identity', None)
        return data


class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            'title',
            'description',
            'category',
            'content_text',
            'content_file',
            'true_identity',
        ]


class VoteSerializer(serializers.ModelSerializer):
    voter = UserSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'voter', 'submission', 'guess', 'created_at']
        read_only_fields = ['submission']
