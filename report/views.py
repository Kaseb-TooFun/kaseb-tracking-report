from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from report import queries
from report.decorators import check_access_to_website


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
    from_date_delta_days = -29
    try:
        from_date_delta_days = int(request.GET.get('from_day', from_date_delta_days))
    except:
        pass

    to_date_delta_days = 0
    try:
        to_date_delta_days = int(request.GET.get('to_day', to_date_delta_days))
    except:
        pass

    days_report = queries.get_days_counts(
        website_id=website_id,
        from_date=datetime.now() + timedelta(days=from_date_delta_days),
        to_date=datetime.now() + timedelta(days=to_date_delta_days),
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
    from_date_delta_days = -29
    try:
        from_date_delta_days = int(request.GET.get('from_day', from_date_delta_days))
    except:
        pass

    to_date_delta_days = 0
    try:
        to_date_delta_days = int(request.GET.get('to_day', to_date_delta_days))
    except:
        pass

    days_report = queries.get_days_counts(
        website_id=website_id,
        from_date=datetime.now() + timedelta(days=from_date_delta_days),
        to_date=datetime.now() + timedelta(days=to_date_delta_days),
        action_id=action_id,
        distinct_session=distinct_session
    )
    response_data['days'] = days_report
    return Response(response_data)
