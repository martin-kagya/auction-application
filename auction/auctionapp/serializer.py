from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Item, Bid, Auction, Watchlist, Payment

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role', 'profile_picture']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields =  ['username', 'email', 'profile', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ItemSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    time_remaining = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['highest_bid', 'bid_count', 'start_time']

    def get_time_remaining(self, obj):
        return obj.time_remaining

class BidSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Bid
        fields = '__all__'
        read_only_fields = ['bid_time']

    def validate(self, data):
        item = data.get('item')
        bid_amount = data.get('bid_amount')
        
        # Check if bid is higher than current highest bid
        if item.highest_bid and bid_amount <= item.highest_bid:
            raise serializers.ValidationError("Bid amount must be higher than current highest bid")
        
        return data

class AuctionSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'
        read_only_fields = ['is_active']

class WatchlistSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Watchlist
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['payment_date', 'is_completed']