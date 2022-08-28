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
        # TODO: Flesh out this method to parse an address string using the
        # parse() method and return the parsed components to the frontend.

        user_input = request.GET['address']

        # TODO implement error handling
        # TODO if data is empty, display message?
        # Does it container characters and numbers?

        address_components, address_type = self.parse(user_input)

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
            return -1, str(e)


