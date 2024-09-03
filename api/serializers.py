from api.models import VerificationV
from rest_framework import serializers


class ParametersSerializer(serializers.ModelSerializer):
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


class DataRequestSerializer(serializers.ModelSerializer):
    Parameters = ParametersSerializer()
    Type = serializers.CharField(max_length=200)


class VerificationVSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationV
        fields = "__all__"
