from rest_framework import serializers
from fuchyRestApi.models import Account, Job
# import djoser

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = Account
        fields = ['email', 'username', 'password','password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Hasła muszą być takie same'})
        account.set_password(password)
        account.save()
        return account

class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'author','category', 'dateStart','price']