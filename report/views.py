from rest_framework.decorators import api_view
from rest_framework.response import Response
from report import queries
from report.decorators import check_access_to_website
from utils import extract_dates_from_request

COUNT_KEYS = [
    "pageViewCount",
    "executeCount",
    "closedCount",
    "clickedCount",
    "conversionRate",
    # "desktopCount",
    # "notDesktopCount",
    "desktopToAllPercent",
]


@api_view(['GET'])
@check_access_to_website
def website_total_report(request, website_id):
    distinct_session = request.GET.get('distinct', '').lower() in ['0', 't', 'true']
    response_data = dict(websiteId=website_id)
    count_data = queries.get_total_counts(website_id, distinct_session=distinct_session)
    total = {}
    for key in COUNT_KEYS:
        total[key] = count_data.get(key, 0)
    response_data['total'] = total
    return Response(response_data)


@api_view(['GET'])
@check_access_to_website
def action_total_report(request, website_id, action_id):
    distinct_session = request.GET.get('distinct', '').lower() in ['0', 't', 'true']
    response_data = dict(
        website_id=website_id,
        action_id=action_id
    )
    count_data = queries.get_total_counts(website_id, action_id, distinct_session=distinct_session)
    total = {}
    for key in COUNT_KEYS:
        total[key] = count_data.get(key, 0)
    response_data['total'] = total
    return Response(response_data)


@api_view(['GET'])
@check_access_to_website
def website_days_report(request, website_id):
    response_data = dict(websiteId=website_id)

    distinct_session = request.GET.get('distinct', '').lower() in ['0', 't', 'true']
    from_date, to_date = extract_dates_from_request(request)

    days_report = queries.get_days_counts(
        website_id=website_id,
        from_date=from_date,
        to_date=to_date,
        distinct_session=distinct_session
    )
    response_data['days'] = days_report
    return Response(response_data)


@api_view(['GET'])
@check_access_to_website
def action_days_report(request, website_id, action_id):
    response_data = dict(
        website_id=website_id,
        action_id=action_id
    )

    distinct_session = request.GET.get('distinct', '').lower() in ['0', 't', 'true']
    from_date, to_date = extract_dates_from_request(request)

    days_report = queries.get_days_counts(
        website_id=website_id,
        from_date=from_date,
        to_date=to_date,
        action_id=action_id,
        distinct_session=distinct_session
    )
    response_data['days'] = days_report
    return Response(response_data)
