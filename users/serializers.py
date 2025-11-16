from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizes the JWT serializer to use 'email' instead of 'username'
    as the authentication field.
    """
    @classmethod
    def get_token(cls, user):
        # The base token is generated here
        token = super().get_token(user)

        # Add custom claims (optional, but useful for frontend)
        token['email'] = user.email
        token['is_admin'] = user.is_admin
        token['is_customer'] = user.is_customer

        return token