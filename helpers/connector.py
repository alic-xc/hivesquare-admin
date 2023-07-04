from json import JSONDecodeError
from django.conf import settings
from pip._vendor import requests
from django.core.exceptions import PermissionDenied


def data_connector(request, endpoint, params, method):
    try:
        token = request.session['staff_session_token']
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    except KeyError:
        headers = {"Content-Type": "application/json", }

    requests_method = getattr(requests, method)
    url = str(settings.API_END_POINT + endpoint)
    response = requests_method(url=url, headers=headers, json=params)
    if response.status_code in settings.SUCCESS_CODES:
        return {
            'success': True,
            'data': response.json()
        }
    elif response.status_code == 409:
        try:
            from account.views import logout
            return logout(request)
        except Exception as err:
            pass
    elif response.status_code == 204:
        return {
            'success': True
        }

    else:
        try:
            return {
                'success': False,
                'data': response.json()
            }

        except JSONDecodeError as error:
            return {
                'success': False,
                'data': 'An error occurred while connecting to the server.'
            }

        except ValueError as error:
            return {
                'success': False,
                'data': error
            }

        except PermissionDenied:
            from account.views import logout
            return logout(request)


def file_connector(request, endpoint, file, method):
    token = request.session['session_token']
    headers = {"Authorization": "Bearer " + token}
    url = str(settings.API_END_POINT + endpoint)
    response = requests.put(url, files=file, headers=headers)
    if response.status_code in settings.SUCCESS_CODES:
        return {
                'success': True,
                'data': response.json()
        }
    else:
        try:
            return {
                'success': False,
                'data': response.json()
            }
        except Exception as error:
            return {
                'success': False,
                'data': error
            }


def file_download_connector(request, endpoint, params, method):
    token = request.session['session_token']
    headers = {"Authorization": "Bearer " + token}
    url = str(settings.API_END_POINT + endpoint)
    response = requests.get(url=url, headers=headers, json=params)
    if response.status_code in settings.SUCCESS_CODES:
        return {
            'success': True,
            'data': response.content
        }
    else:
        try:
            return {
                'success': False,
                'data': response.json()
            }
        except Exception as error:
            return {
                'success': False,
                'data': error
            }

