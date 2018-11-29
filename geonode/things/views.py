# from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseServerError
from django.shortcuts import redirect, render # , get_object_or_404
import json, requests
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':DHE-RSA-AES256-GCM-SHA384'

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

def _get_token(auth_url, auth_headers):
    '''
    Get JSON web token from Thingsboard tenant credentials
    '''
    username = 'citydata@unsw.edu.au'
    password = 'U,V3Va'

    auth_data = json.dumps({
        'username': username,
        'password': password
    })

    import logging
    logger = logging.getLogger("geonode.things.views")

    logger.debug('B4 requesting JWT, auth_url: ' + auth_url)
    logger.debug('B4 requesting JWT, Content-Type: ' + auth_headers['Content-Type'])
    logger.debug('B4 requesting JWT, Accept: ' + auth_headers['Accept'])
    logger.debug('B4 requesting JWT, auth_data: ' + auth_data)
    # logger.handlers[0].flush()

    response = requests.post(auth_url, headers=auth_headers, data=auth_data, verify=False)

    if response.status_code == 200:
        return response.json()['token']
    else:
        logger.error('Error fetching JWT, status code: ' + str(response.status_code))
        return

def myair_latest(request, id, in_key='C02'):
    '''
    Get latest CO2 data from a device
    '''

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    # Set fixed URL request parameters
    protocol = 'https'
    host = 'citysensors.be.unsw.edu.au'
    api_path = 'api'
    auth_path = 'auth/login'
    device_path = 'plugins/telemetry/DEVICE'

    url_base = protocol + '://' + '/'.join([host, api_path])

    headers['X-Authorization'] = 'Bearer ' + _get_token('/'.join([url_base, auth_path]), headers)

    ts_path = 'values/timeseries'

    ftr = _get_myair_feature(id)
    device_id = ftr['properties']['DeviceID']

    # Correct typo in parameter name
    if in_key == 'C02':
        out_key = 'CO2'
    else:
        out_key = in_key

    # Read latest data for device
    key_query = 'keys=' + in_key

    url = '/'.join([url_base, device_path, device['id'], ts_path]) + '?' + key_query

    response = requests.get(url, headers=headers)

    data = response.json()

    data[out_key] = data.pop(in_key)

    return data
