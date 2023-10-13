from gettext import find
from typing import Self
import requests
import urllib


class IdealPostcodes:
    def request( url ='' , query_parameters = {}):
        base_url = "https://api.ideal-postcodes.co.uk/v1/autocomplete/addresses"
        query_parameters.update({'api_key': ''})
        encoded = urllib.parse.urlencode(query_parameters)
        payload={}
        headers = {
        'Accept': 'application/json'
        }
        response = requests.request("GET", f"{base_url}{url}?{encoded}", headers=headers, data=payload)
        return response.json()

    def getSugestions(consulta):
        query_parameters = { 'context': 'BRA',
                            'query': consulta
                            }
        response = IdealPostcodes.request('',  query_parameters)
        if  response['code'] == 2000 and len(response['result']['hits']) >= 0:
            return response['result']['hits'][0]['id']
        return False

    def getAddress(id):
        url = f"/{id}/gbr"
        return IdealPostcodes.request(url)

    def find(consulta):
        id_address = IdealPostcodes.getSugestions(consulta)
        if id_address:
            return IdealPostcodes.getAddress(id_address)
        return False

