from copy import deepcopy
from datetime import timedelta, datetime

from utils import get_mongodb_client

mongo_client = get_mongodb_client()

EVENTS = 'events'
DATE_FIELD = 'eventTime'

DAYS_COUNT_KEYS = [
    'pageViewCount',
    'executeCount',
    'closedCount',
    'clickedCount',
    'conversionRate',
]


def calculate_conversion_rate(results_data):
    conversion_rate = 0
    if results_data.get("executeCount", 0) > 0:
        conversion_rate = int(
            results_data.get("clickedCount", 0) / results_data.get("executeCount") * 100
        )
    return conversion_rate


def get_total_counts(website_id, action_id=None, distinct_session=False):
    website_db = mongo_client[website_id]
    events = website_db[EVENTS]

    if distinct_session:
        # todo
        pass
    page_view_filter = {
        "event": {"$in": ["PAGE_VIEW"]}
    }
    execute_filter = {
        "event": {"$in": ["BANNER_SHOW", "ANIMATION_RUN"]}
    }
    close_filter = {
        "event": {"$in": ["BANNER_CLOSE"]}
    }
    click_filter = {
        "event": {"$in": ["BANNER_BUTTON_CLICK", "ANIMATION_CLICK_ITEM"]}
    }
    desktop_filter = {
        "categoricalProps.deviceType": {"$exists": True, "$in": ["Desktop"]}
    }

    not_desktop_filter = {
        "categoricalProps.deviceType": {"$exists": True, "$not": {"$in": ["Desktop"]}}
    }

    if action_id:
        page_view_filter["targetEntityId"] = {"$in": [action_id]}
        execute_filter["targetEntityId"] = {"$in": [action_id]}
        close_filter["targetEntityId"] = {"$in": [action_id]}
        click_filter["targetEntityId"] = {"$in": [action_id]}
        desktop_filter["targetEntityId"] = {"$in": [action_id]}
        not_desktop_filter["targetEntityId"] = {"$in": [action_id]}

    pipeline = [
        {"$facet": {
            "pageViewCount": [
                {"$match": page_view_filter},
                {"$count": "pageViewCount"}
            ],
            "executeCount": [
                {"$match": execute_filter},
                {"$count": "executeCount"},
            ],
            "closedCount": [
                {"$match": close_filter},
                {"$count": "closedCount"}
            ],
            "clickedCount": [
                {"$match": click_filter},
                {"$count": "clickedCount"}
            ],
            "desktopCount": [
                {"$match": desktop_filter},
                {"$count": "desktopCount"}
            ],
            "notDesktopCount": [
                {"$match": not_desktop_filter},
                {"$count": "notDesktopCount"}
            ],
        }},
        {"$project": {
            "pageViewCount": {"$arrayElemAt": ["$pageViewCount.pageViewCount", 0]},
            "executeCount": {"$arrayElemAt": ["$executeCount.executeCount", 0]},
            "closedCount": {"$arrayElemAt": ["$closedCount.closedCount", 0]},
            "clickedCount": {"$arrayElemAt": ["$clickedCount.clickedCount", 0]},
            "desktopCount": {"$arrayElemAt": ["$desktopCount.desktopCount", 0]},
            "notDesktopCount": {"$arrayElemAt": ["$notDesktopCount.notDesktopCount", 0]}
        }}
    ]

    aggregate_results = events.aggregate(pipeline)

    results = {}
    try:
        results = list(aggregate_results)[0]
    except IndexError:
        pass

    conversion_rate = calculate_conversion_rate(results)
    results["conversionRate"] = conversion_rate

    desktopToAllPercent = 0
    desktopCount = results.get("desktopCount", 0)
    notDesktopCount = results.get("notDesktopCount", 0)
    _all_count = desktopCount + notDesktopCount
    if _all_count > 0:
        desktopToAllPercent = int(desktopCount / _all_count * 100)
    results["desktopToAllPercent"] = desktopToAllPercent

    return results


def get_days_counts(website_id, from_date, to_date, action_id=None, distinct_session=False):
    assert isinstance(from_date, datetime)
    assert isinstance(to_date, datetime)
    website_db = mongo_client[website_id]
    events = website_db[EVENTS]

    if distinct_session:
        # todo
        pass

    page_view_event_types = ["PAGE_VIEW"]
    execute_event_types = ["BANNER_SHOW", "ANIMATION_RUN"]
    close_event_types = ["BANNER_CLOSE"]
    click_event_types = ["BANNER_BUTTON_CLICK", "ANIMATION_CLICK_ITEM"]
    # execute_filter = {
    #     "event": {"$in": ["BANNER_SHOW", "ANIMATION_RUN"]}
    # }
    # close_filter = {
    #     "event": {"$in": ["BANNER_CLOSE"]}
    # }
    # click_filter = {
    #     "event": {"$in": ["BANNER_BUTTON_CLICK", "ANIMATION_CLICK_ITEM"]}
    # }

    filters = {
        "eventTime": {
            "$gte": datetime(from_date.year, from_date.month, from_date.day),
            "$lt": datetime(to_date.year, to_date.month, to_date.day) + timedelta(days=1)
        }
    }
    if action_id:
        filters["targetEntityId"] = {"$in": [action_id]}

    pipeline = [
        {
            "$match": filters
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y/%m/%d",
                        "date": f"${DATE_FIELD}"
                    }
                },
                # "count": {"$sum": 1},
                "pageViewCount": {
                    "$sum": {"$cond": [{"$in": ["$event", page_view_event_types]}, 1, 0]}
                },
                "executeCount": {
                    "$sum": {"$cond": [{"$in": ["$event", execute_event_types]}, 1, 0]}
                },
                "closedCount": {
                    "$sum": {"$cond": [{"$in": ["$event", close_event_types]}, 1, 0]}
                },
                "clickedCount": {
                    "$sum": {"$cond": [{"$in": ["$event", click_event_types]}, 1, 0]}
                },
            }
        },
        {"$sort": {"_id": 1}}
    ]

    aggregate_results = events.aggregate(pipeline)

    _results = []
    try:
        _results = list(aggregate_results)
    except Exception as ex:
        print(f'Exception in get_days_counts: {ex}')

    day_date_to_result_dict = {
        result_dict.get('_id'): result_dict
        for result_dict in _results
    }
    results = []
    day_date = deepcopy(from_date)
    while day_date <= to_date:
        day_str = day_date.strftime('%Y/%m/%d')
        day_data_dict = day_date_to_result_dict.get(day_str, {})
        conversion_rate = calculate_conversion_rate(day_data_dict)
        day_data_dict["conversionRate"] = conversion_rate
        cleaned_day_data = {
            key: day_data_dict.get(key, 0)
            for key in DAYS_COUNT_KEYS
        }
        cleaned_day_data['day'] = day_str
        results.append(cleaned_day_data)
        day_date += timedelta(days=1)

    return results
