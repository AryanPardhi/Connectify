from rest_framework import serializers
from .models import FriendRequest

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['recipient', 'status'] 
        extra_kwargs = {
            'status': {'default': 'pending'}  
        }

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user  
        return super().create(validated_data)
    
    def validate(self, data):
        sender = self.context['request'].user
        recipient = data.get('recipient')
        
        if sender == recipient:
            raise serializers.ValidationError("You cannot send a friend request to yourself.")

        return data
    
    
class PendingRequestSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    recipient = serializers.CharField(source='recipient.username', read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['sender', 'recipient', 'status','created_at']