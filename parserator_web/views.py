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

        print("The address entered was: ")
        print(user_input)

        # TODO implement error handling
        # Does it container characters and numbers?
        # 
        address_components, address_type = self.parse(user_input)

        print("Here is the address type: ")
        print(address_type)
        print("and here is the address components: ")
        print(address_components)

        return Response({'input_string': user_input,
                        'address_components': address_components,
                        'address_type': address_type})

    def parse(self, address):
        # usaddress documentation: https://github.com/datamade/usaddress
        # usaddress.tag returns the address components followed by the address type
        tagged_address = usaddress.tag(address)
        address_components = tagged_address[0]
        address_type = tagged_address[1]

        return address_components, address_type
