from rest_framework.response import Response
from rest_framework.views import APIView

from .controller.training import TrainingHelper, CommentHelper, LikeHelper, CommentReplyHelper
from django.views.decorators.csrf import csrf_exempt

class TrainingView(APIView):
    @csrf_exempt
    def post(self, request):
        obj = TrainingHelper(request)
        response, status = obj.post()
        return Response(response, status=status)


class CommentView(APIView):
    def get(self, request):
        obj = CommentHelper(request)
        response, status = obj.get()
        return Response(response, status=status)

    def post(self, request):
        obj = CommentHelper(request)
        response, status = obj.post()
        return Response(response, status=status)


class CommentReplyView(APIView):
    def get(self, request):
        obj = CommentReplyHelper(request)
        response, status = obj.post()
        return Response(response, status=status)

    def post(self, request):
        obj = CommentReplyHelper(request)
        response, status = obj.post()
        return Response(response, status=status)


class LikeView(APIView):
    def get(self, request):
        obj = LikeHelper(request)
        response, status = obj.get()
        return Response(response, status=status)

    def post(self, request):
        obj = LikeHelper(request)
        response, status = obj.post()
        return Response(response, status=status)

