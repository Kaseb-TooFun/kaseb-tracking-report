import json

from django.conf import settings
from django.http import HttpResponse
from utils import get_admin_key, check_access_to_website_by_api_call

ADMIN_KEY = get_admin_key()


def check_access_to_website(function):
    def wrapper(request, *args, **kwargs):
        # user = request.user
        website_id = kwargs.get('website_id')
        dont_permission_response = HttpResponse(
            json.dumps(dict(
                message="You dont have permission.",
                website_id=website_id
            )),
            content_type="application/json",
            status=403
        )
        if not website_id:
            return dont_permission_response

        authorization_value = request.headers.get('Authorization')
        if settings.DEBUG:
            print(f'website_id: {website_id} - authorization_value: {authorization_value}')

        has_access = False
        if authorization_value and ADMIN_KEY and authorization_value == ADMIN_KEY:
            has_access = True

        # check authentication header by call website api
        has_access = check_access_to_website_by_api_call(website_id, authorization_value)

        if has_access:
            return function(request, *args, **kwargs)
        else:
            return dont_permission_response
    return wrapper
