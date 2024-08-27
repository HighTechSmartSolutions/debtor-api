from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
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
            ClientV.objects.get(ip=request.META['HTTP_X_REAL_IP'])
        except KeyError:
            return Response(
                'IP can not be recieved',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = ActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        filter = {field: value for field, value 
                  in serializer.validated_data.items() if value}
        
        if not filter:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        debtor_cards = VerificationV.objects.filter(**filter)\
                                            .distinct()
        if not debtor_cards:
            return Response(status.HTTP_204_NO_CONTENT)
        
        serializer = VerificationVSerializer(debtor_cards, many=True)
        return Response(serializer.data)
        

class DataValidation(APIView):
    def post(self, request):
        # try:
        #     client_IP=request.META['HTTP_X_REAL_IP']
        #     ClientV.objects.get(ip=client_IP)
        # except KeyError:
        #     return Response(
        #         'IP can not be recieved',
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # except ObjectDoesNotExist:
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        client_IP = '111'
        
        serializer = ActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        params = f'''
            @p_id={serializer.validated_data['id'] or 'null'},
            @p_phone_number={serializer.validated_data['phone_number']},
            @p_email={serializer.validated_data['email']},
            @p_persons_identity_card1={serializer.validated_data['persons_identity_card1']},
            @p_persons_identity_card2={serializer.validated_data['persons_identity_card2']},
            @p_application_date={serializer.validated_data['application_date'] or 'null'},
            @p_client_IP={client_IP}'''


        with connection.cursor() as cursor:
            cursor.execute(f'EXEC dbo.spap_req_verif {params}')
            return(Response(cursor.fetchall()))
