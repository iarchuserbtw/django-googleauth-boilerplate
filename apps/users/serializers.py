from rest_framework import serializers


from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'display_name', 'phone', 'email',
            'created_at', 'updated_at',
            'last_activity', 
            'is_active', 'is_staff'
        )
        read_only_fields = ('created_at', 'updated_at', 'last_activity')

    def create(self, validated_data):
        username = validated_data.get('username')
        print(username)
        return User.objects.create(**validated_data)