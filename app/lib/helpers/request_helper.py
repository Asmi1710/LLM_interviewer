import requests
from flask import current_app
from app.lib.helpers import random_string
from app.lib.helpers.flask_helper import current_request_id

def get(url, headers={}):
    headers = set_headers(headers)

    current_app.logger.info(f"Making GET call to {url}")
    current_app.logger.info(f"HEADERS: {headers}")

    response = requests.get(f"{url}", headers=headers)
    validate_response_status(response)
    response_json = response.json()

    current_app.logger.info(f"Finished GET call {url}")
    current_app.logger.info(f"RESPONSE: {response_json}")

    return response_json

def post(url, data, headers={}, timeout=10):
    headers = set_headers(headers)

    current_app.logger.info(f"Making POST call to {url}")
    current_app.logger.info(f"HEADERS: {headers}")
    current_app.logger.info(f"REQUEST: {data}")

    response = requests.post(f"{url}", json=data, headers=headers, timeout=timeout)
    validate_response_status(response)
    response_json = response.json()

    current_app.logger.info(f"Finished POST call {url}")
    current_app.logger.info(f"RESPONSE: {response_json}")

    return response_json

def validate_response_status(response):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        current_app.logger.error(f"Http Error: {e}")
        raise e
    except requests.exceptions.ConnectionError as e:
        current_app.logger.error(f"Error Connecting: {e}")
        raise e
    except requests.exceptions.ReadTimeout as e:
        current_app.logger.error(f"Timeout Error: {e}")
        raise e
    except requests.exceptions.Timeout as e:
        current_app.logger.error(f"Timeout Error: {e}")
        raise e
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"OOps: Something Else {e}")
        raise e

def set_headers(headers):
    headers['caller_id'] = 'experts_backend'
    headers['X-Request-Id'] = current_request_id() or f'experts-{random_string(stringLength=16)}'
    return headers
    