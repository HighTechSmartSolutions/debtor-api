import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from api.models import VerificationV, ClientV
from rest_framework.response import Response
from rest_framework.views import APIView, status
from api.serializers import DataRequestSerializer, VerificationVSerializer


logger = logging.getLogger(__name__)

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
        
        logger.info('Start IP validation')
        try:
            client_IP=request.META['HTTP_X_CLIENT_IP']
        except KeyError:
            logger.exception('Meta key error')
            return Response('IP can not be recieved',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        logger.info(f'Client IP - {client_IP}')
        try:
            ClientV.objects.get(ip=client_IP)
        except ObjectDoesNotExist:
            logger.exception('IP is not set in the DB')
            return Response(status=status.HTTP_403_FORBIDDEN)
        logger.info('IP validation completed')
        
        serializer = DataRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        parameters = serializer.validated_data['Parameters']
        
        params = (parameters['id'],
                  parameters['phone_number'],
                  parameters['email'],
                  parameters['persons_identity_card1'],
                  parameters['persons_identity_card2'],
                  parameters['application_date'],
                  client_IP,
                  serializer.validated_data['Type'])

        sql_request = 'EXEC dbo.spap_req_verif %s,%s,%s,%s,%s,%s,%s,%s'

        with connection.cursor() as cursor:
            cursor.execute(sql_request, params)
            return(Response(cursor.fetchall()))
