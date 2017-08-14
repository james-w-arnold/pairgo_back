from rest_framework import serializers
from matching.models import Match
from .models import Thread, ThreadUser, Message
from accounts.models import User

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', )

class ThreadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadUser
        exclude = ('id', )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)

class ThreadSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    recipients = UserSerializer(many=True)

    class Meta:
        model = Thread
        fields = ('name', 'match', 'recipients')

    def create(self, validated_data):
        recipients = validated_data.pop('recipients')
        thread = Thread(name=validated_data['name'], match=validated_data['match'])
        thread.save()

        for recipient in recipients:
            new_user = ThreadUser(user=recipients, thread=thread)
            new_user.save()

        return thread


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('id', )
