from audioop import add
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

        address_components, address_type = self.parse(user_input)

        # If there was an error, address_components will be -1 and
        # address_type will contain an error message that can be displayed
        # to the user
        return Response({'input_string': user_input,
                        'address_components': address_components,
                        'address_type': address_type})

    def parse(self, address):
        # usaddress documentation: https://github.com/datamade/usaddress
        # usaddress.tag returns the address components followed by the address type
        try:
            address_components, address_type = usaddress.tag(address)
            return address_components, address_type
        except usaddress.RepeatedLabelError as e:
            error_string = "ERROR: Unable to tag this string because more than one area of the string has the same label"
            return -1, error_string


