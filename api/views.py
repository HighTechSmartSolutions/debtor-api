from django.core.exceptions import ObjectDoesNotExist
from api.models import VerificationV, ClientV
from rest_framework.response import Response
from rest_framework.views import APIView, status
from api.serializers import ActionSerializer, VerificationVSerializer


class Action(APIView):
    '''
    Validate request and return data from db

    Request:
    {
        'id': id,
        'phone_number': phone_number,
        'email': email,
        'persons_identity_card1': persons_identity_card1,
        'persons_identity_card2': persons_identity_card2,
        'application_date': application_date,
    }

    Return:
    debtor_cards with requested parameters.

    '''
    def post(self, request):
        print(request.META)
        try:
            ClientV.objects.using('debthor_dbs')\
                           .get(ip=request.META['HTTP_X_REAL_IP'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = ActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        filter = {field: value for field, value 
                  in serializer.validated_data.items() if value}
        if not filter:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        debtor_cards = VerificationV.objects.using('debthor_dbs')\
                                            .filter(**filter)\
                                            .distinct()
        if not debtor_cards:
            return Response(status.HTTP_204_NO_CONTENT)
        
        serializer = VerificationVSerializer(debtor_cards, many=True)
        return Response(serializer.data)
        
        
