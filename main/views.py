from .models import Purchase, Buyer
from .serializer import GetSerializersList, SerializersCreate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
# Create your views here.
from rest_framework.parsers import BaseParser
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
import csv


class CSVTextParser(BaseParser):
    media_type = 'multipart/form-data'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Return a list of lists representing the rows of a CSV file.
        """
        media_type_params = dict([param.strip().split('=') for param in media_type.split(';')[1:]])
        charset = media_type_params.get('charset', 'utf-8')
        txt = stream.FILES.get('file').read().decode(charset)
        csv_table = list(csv.DictReader(txt.splitlines()))
        return csv_table


class AplPost(viewsets.ModelViewSet):
    parser_classes = [CSVTextParser]
    queryset = Purchase.objects.all()
    serializer_class = SerializersCreate

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid()
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'status': 'ok'}, status=status.HTTP_200_OK, headers=headers)

        return Response({'Status': 'Error', 'Desc':serializer.errors}, status=status.HTTP_400_BAD_REQUEST )


class AplGet(ListAPIView):
    serializer_class = GetSerializersList

    def get_queryset(self):
        buyer = Buyer.objects.all().order_by('-spent_money')[:5]
        return buyer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"response": serializer.data})
