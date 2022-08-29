import pytest
from django.urls import reverse
import json

def test_api_parse_succeds(client):
    # Send a request to the API and confirm that the
    # data comes back in the appropriate format.
    address_string = '123 main st chicago il'
    url = reverse('address-parse')
    data = {"address": address_string}

    response = client.get(url,data)

    correct_response_data = ({'address_components': {'AddressNumber': '123',
                                                    'PlaceName': 'chicago',
                                                    'StateName': 'il',
                                                    'StreetName': 'main',
                                                    'StreetNamePostType': 'st'},
                            'address_type': 'Street Address',
                            'input_string': '123 main st chicago il',
    })

    assert response.status_code == 200
    assert json.loads(response.content) == correct_response_data


def test_api_parse_raises_error(client):
    # The address_string below will raise a
    # RepeatedLabelError, so ParseAddress.parse() will not be able to parse it.
    address_string = '123 main st chicago il 123 main st'
    url = reverse('address-parse')
    data = {"address": address_string}

    response = client.get(url,data)    

    correct_response_data = ({'address_components': -1,
                                'address_type': 'ERROR: Unable to tag this string because more than one area of the string has the same label',
                                'input_string': '123 main st chicago il 123 main st',
    })

    assert json.loads(response.content) == correct_response_data
