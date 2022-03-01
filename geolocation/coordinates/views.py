import json
import requests
from dicttoxml import dicttoxml
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# Create your views here.

@api_view(('POST',))
def getAddressDetails(request):
    try:
        # Google GeoCoding Key 
        key = 'AIzaSyCOD3KvY2DDzEfel-NZ_LKIWXr86EF_EUw'
        
        # Pull the body data 
        request_payload = request.data
        address = request_payload.get('address')
        output_format = request_payload.get('output_format')

        
        # return bad request, if either of parameter is not found.
        if not all([address, output_format]):
            return Response('Expected parameter not found', status=status.HTTP_400_BAD_REQUEST)

        # Create payload for geolocation api.
        payload = {
            'key': key,
            'address': address
        }

        res = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=payload)
        json_res = json.loads(res.text)
        
        if not json_res.get('results'):
            return Response('Provided address not found!', status=status.HTTP_400_BAD_REQUEST)

        location = json_res.get('results')[0].get('geometry').get('location')

        resp_obj = {
            "coordinates": {
                "lat": location.get('lat'),
                "lng": location.get('lng')
            },
            "address": payload.get('address')
        }

        xml = dicttoxml(resp_obj)
        
        if output_format.lower() == 'json':
            return Response(resp_obj)
        elif output_format.lower() == 'xml':
            return Response(xml)
        else:
            return Response('Output format should be either json or xml', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response('Exception Occured', status=status.HTTP_500_INTERNAL_SERVER_ERROR)