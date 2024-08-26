from api.models import VerificationV
from rest_framework.serializers import ModelSerializer


class ActionSerializer(ModelSerializer):
    class Meta:
        model = VerificationV
        fields = [
            'id',
            'phone_number',
            'email',
            'persons_identity_card1',
            'persons_identity_card2',
            'application_date'
        ]
        extra_kwargs = {'id': {'read_only': False, 'allow_null': True},
                        'phone_number': {'required': True},
                        'email': {'required': True},
                        'persons_identity_card1': {'required': True},
                        'persons_identity_card2': {'required': True},
                        'application_date': {'required': True}}


class VerificationVSerializer(ModelSerializer):
    class Meta:
        model = VerificationV
        fields = "__all__"
