from rest_framework import views
from rest_framework.response import Response


class order(views.APIView):

        def post(self, request, *args, **kwargs):

            return Response({'success': True, 'status': 400, 'message': 'Email not found.please register first'})


