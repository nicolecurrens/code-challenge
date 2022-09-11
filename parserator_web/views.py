from audioop import add
from rest_framework import status
import usaddress
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ParseError


class Home(TemplateView):
    template_name = 'parserator_web/index.html'


class AddressParse(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        # Grab address from get request
        user_input = request.GET['address']

        try:
            address_components, address_type = self.parse(user_input)
            return Response({'input_string': user_input,
                        'address_components': address_components,
                        'address_type': address_type},
                        status=status.HTTP_200_OK)
        except:
            # If an error is raised from usaddress, return a 400 response
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def parse(self, address):
        # usaddress documentation: https://github.com/datamade/usaddress
        # usaddress.tag returns the address components followed by the address type
        try:
            address_components, address_type = usaddress.tag(address)
            return address_components, address_type
        except usaddress.RepeatedLabelError as e:
            raise


