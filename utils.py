import os
import pymongo
from django.conf import settings
from pip._vendor import requests

MONGO_CONFIG_KEY = 'MONGO_CONFIG'
ADMIN_KEY_KEY = 'ADMIN_KEY'
BACKEND_BASE_URL_KEY = 'BACKEND_BASE_URL'


def get_mongodb_client():
    mongo_config = os.getenv(MONGO_CONFIG_KEY)
    if not mongo_config:
        raise Exception(f"{MONGO_CONFIG_KEY} is required env variable for connecting to mongodb.")
    if not mongo_config.startswith('mongodb://'):
        mongo_config = f'mongodb://{mongo_config}'
    mongo_client = pymongo.MongoClient(mongo_config)
    return mongo_client


def get_admin_key():
    admin_key = os.getenv(ADMIN_KEY_KEY)
    return admin_key


def get_backend_base_url():
    base_url = os.getenv(BACKEND_BASE_URL_KEY)
    return base_url


def check_access_to_website_by_api_call(website_id, authorization_value):
    base_url = get_backend_base_url()
    url = f'{base_url}/api/v1/websites/{website_id}'
    headers = {
        'Authorization': authorization_value
    }
    request = requests.get(
        url,
        headers=headers
    )
    if settings.DEBUG:
        print(f'call website api => url: {url} | status: {request.status_code} | response: {request.text}')

    has_access = bool(request.status_code == 200)
    return has_access
