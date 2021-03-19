from rest_framework.response import Response
from rest_framework.views import APIView

from .controller.refer_friend import ReferFriendHelper


class ReferFriendView(APIView):
    def post(self, request):
        obj = ReferFriendHelper(request)
        response, status = obj.post()
        return Response(response, status=status)
