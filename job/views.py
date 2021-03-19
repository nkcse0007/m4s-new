from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ContactUs
from .serializers import ContactUsSerializer
from .controller.jobs import RequestTalentHelper, SubmitJobHelper, SubmitCvHelper, SearchJobHelper, FieldHelper, \
    SearchAllHelper
from rest_framework.generics import ListCreateAPIView


class RequestTalentView(APIView):
    def post(self, request):
        obj = RequestTalentHelper(request)
        response, status = obj.post()
        return Response(response, status=status)


class SubmitJobView(APIView):

    def get(self, request):
        obj = SubmitJobHelper(request)
        response, status = obj.get()
        return Response(response, status=status)

    def post(self, request):
        obj = SubmitJobHelper(request)
        response, status = obj.post()
        return Response(response, status=status)


class SubmitCvView(APIView):
    def post(self, request):
        obj = SubmitCvHelper(request)
        response, status = obj.post()
        return Response(response, status=status)


class SearchJobView(APIView):

    def post(self, request):
        obj = SearchJobHelper(request)
        response, status = obj.post()
        return Response(response, status=status)


class SearchAll(APIView):

    def get(self, request):
        obj = SearchAllHelper(request)
        response, status = obj.get()
        return Response(response, status=status)


class FieldsView(APIView):
    def get(self, request):
        obj = FieldHelper(request)
        response, status = obj.get()
        return Response(response, status=status)


class ContactView(ListCreateAPIView):
    model = ContactUs
    queryset = model.objects.all()
    serializer_class = ContactUsSerializer
