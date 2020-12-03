import json
from pprint import pprint

from utils import get_mongodb_client
import os
from datetime import datetime, timedelta

import pymongo


EVENTS = 'events'


def is_config_id(id):
    return bool(id.count('-') >= 4)


my_client = get_mongodb_client()


def find_active_configs():
    db_list = my_client.list_database_names()
    for db in db_list:
        if is_config_id(db):
            my_db = my_client[db]
            # collection_list = my_db.list_collection_names()
            # print(f'{db} - {collection_list}')
            my_events = my_db[EVENTS]
            x = my_events.find_one()
            print(f'{db}: {x}')


def check_config_events(website_id):
    my_db = my_client[website_id]
    my_events = my_db[EVENTS]
    # one = my_events.find_one()
    # print(f'find one: {one}')
    start_dt = datetime(2020, 10, 9)
    query = dict()
    # query["eventTime"] = {"$gte": start_dt, "$lt": start_dt + timedelta(days=1)}
    query["event"] = {"$in": ["BANNER_SHOW", "ANIMATION_RUN"]}

    for i, ev in enumerate(
            list(
                my_events.find(query).distinct("entityId")
            )
    ):
        print(f'event {i+1}: {ev}')

    property = "entityId"
    events = my_events.find(
        query,
        # {"_id": 0, property: 1}
    )

    ev2cnt = dict()
    for i, evd in enumerate(events):
        print(f'{i}: {evd}')
        ev = evd.get(property)
        ev2cnt[ev] = ev2cnt.get(ev, 0) + 1
        # et = evd.get("eventTime")
        # print(et)

    print(f'{property} to counts:\n {json.dumps(ev2cnt, indent=4)}')


# find_active_configs()

active_website_id = "7bba2f99-75a2-43b6-8f0f-0ad882f10d8a"
active_action_id = "0e640251-bdc4-4264-a557-011d9a5d41f7"
check_config_events(active_website_id)

# =========== queries =============
from report import queries

# results = queries.get_total_counts(
#     active_website_id,
#     # active_action_id,
#     distinct_session=True,
# )
# pprint(results)

results = queries.get_days_counts(
    website_id=active_website_id,
    from_date=datetime(2020, 1, 9),
    to_date=datetime(2020, 12, 9),
    # action_id=active_action_id,
    distinct_session=True
)
pprint(results)
