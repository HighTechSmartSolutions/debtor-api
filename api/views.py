import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from api.models import VerificationV, ClientV
from rest_framework.response import Response
from rest_framework.views import APIView, status
from api.serializers import ActionSerializer, VerificationVSerializer


logger = logging.getLogger(__name__)


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
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        fmtstr = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
        fmtdate = '%H:%M:%S'
        formater = logging.Formatter(fmtstr, fmtdate)
        ch.setFormatter(formater)
        logger.addHandler(ch)
        
        logger.warning('Start DataValidation')
        try:
            print(request.META)
            logger.warning(f'{key} --- {value}\n' for key, value in request.META.items())
            client_IP=request.META['X-Client-IP']
            ClientV.objects.get(ip=client_IP)
        except KeyError:
            logger.exception('Ошибка в DataValidation')
            return Response(
                'IP can not be recieved',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = ActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # client_IP = '111'
        
        params = (serializer.validated_data['id'],
                  serializer.validated_data['phone_number'],
                  serializer.validated_data["email"],
                  serializer.validated_data['persons_identity_card1'],
                  serializer.validated_data['persons_identity_card2'],
                  serializer.validated_data['application_date'],
                  client_IP)

        sql_request = 'EXEC dbo.spap_req_verif %s,%s,%s,%s,%s,%s,%s'

        with connection.cursor() as cursor:
            cursor.execute(sql_request, params)
            return(Response(cursor.fetchall()))
