# from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseServerError
from django.shortcuts import redirect, render # , get_object_or_404
import requests
import json

def _get_myair_feature(id):
    '''
    Get attributes of myair device from myair by WFS
    '''
    protocol = 'https'
    host = 'citydata.be.unsw.edu.au'
    username = 'jondoig'
    passwd = ']gy(WMob*m5|'
#     propertyName = 'ID,deviceID,DashURL'
    path = 'geoserver/wfs'
    typename = 'geonode:myair'
    cql_filter = 'ID=' + "'" + str(id) + "'"

    url = (protocol + '://' + host + '/' + path + '?'
        + 'request=GetFeature'
        + '&outputFormat=json'
        + '&typename=' + typename
#         + '&propertyName=' + propertyName
        + '&cql_filter=' + cql_filter
       )
    response = requests.get(url, auth=(username, passwd))
    if response.status_code == 200:
        feature = json.loads(response.text)['features'][0]
        return feature
    else:
        logger.error('Error fetching feature, status code: ' + str(response.status_code))
        return

def myair_dashboard(request, id):
    ftr = _get_myair_feature(id)
    dash_url = ftr['properties']['DashURL']
    return redirect(dash_url)

def myair_view(request, id, template='myair/index.html'):
    '''
    View myair as html
    '''
    return render(request, template)

# def myair_latest(request, id, key='C02'):
