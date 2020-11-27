- به ازای هر سایت یه db داریم

- "entityId" : "site-user-id",
- هرکسی که میره تو یه سایت بازدید میکنه یه کوکی براش ست میشه

- "targetEntityId" : "config-id",

- find one: 
```
{
    '_id': ObjectId('5f5610a918339f8f5c783348'),
    'eventId': None, 'event': 'BANNER_SHOW', 'entityType': 'user', 
    'entityId': '4f6ee122-2b43-4c92-8392-d33057de2530', 
    'targetEntityId': '0e640251-bdc4-4264-a557-011d9a5d41f7', 
    'dateProps': {}, 
    'categoricalProps': {'OS': ['UNIX'], 'deviceType': ['Desktop'], 'borwser': ['Chrome'], 'borwserVer': ['85.0.4183.83']}, 
    'floatProps': {}, 'booleanProps': {}, 
    'eventTime': datetime.datetime(2020, 9, 7, 10, 51, 20)
}
```

- GOAL, BANNER_SHOW, BANNER_CLOSE, BANNER_BUTTON_CLICK, BANNER_PREVIEW_TIME,
    ANIMATION_RUN, ANIMATION_CLICK_ITEM, NEW_USER_REGISTER, SESSION_DURATION

- دیتای آمار تو این فرمت باشه
- اولی آمار کلی
- دومی آمار ۳۰ روز گذشته



```js
demoCountsStatistics = {
    displayCount: 30640,
    executeCount: 20480,
    conversionRate: 67,
    sessionCount: 10240,
    seenCount: 5120,
    closedCount: 5120,
    clickedCount: 5120,
    desktopToMobilePercent: 65,
}

last30DayStatistics = [
    {
        displayCount: 333,
        executeCount: 305,
        sessionCount: 164,
        seenCount: 113,
        closedCount: 130,
        clickedCount: 140,
    },
    // 30 element
]
```

find one: {'_id': ObjectId('5f5610a918339f8f5c783348'), 'eventId': None, 'event': 'BANNER_SHOW', 'entityType': 'user', 'entityId': '4f6ee122-2b43-4c92-8392-d33057de2530', 'targetEntityId': '0e640251-bdc4-4264-a557-011d9a5d41f7', 'dateProps': {}, 'categoricalProps': {'OS': ['UNIX'], 'deviceType': ['Desktop'], 'borwser': ['Chrome'], 'borwserVer': ['85.0.4183.83']}, 'floatProps': {}, 'booleanProps': {}, 'eventTime': datetime.datetime(2020, 9, 7, 10, 51, 20)}
event to counts:
 {
    "BANNER_SHOW": 32,
    "BANNER_CLOSE": 7,
    "NEW_USER_REGISTER": 38
}


- http://127.0.0.1:8000/api/report/total/website/7bba2f99-75a2-43b6-8f0f-0ad882f10d8a
- http://127.0.0.1:8000/api/report/total/website/7bba2f99-75a2-43b6-8f0f-0ad882f10d8a/action/0e640251-bdc4-4264-a557-011d9a5d41f7
- http://127.0.0.1:8000/api/report/days/website/7bba2f99-75a2-43b6-8f0f-0ad882f10d8a
- http://127.0.0.1:8000/api/report/days/website/7bba2f99-75a2-43b6-8f0f-0ad882f10d8a/action/0e640251-bdc4-4264-a557-011d9a5d41f7

### endpoints
- /api/report/total/website/website_id
- /api/report/total/website/website_id/action/action_id
- /api/report/days/website/website_id?from_day=-29&to_day=0
- /api/report/days/website/website_id/action/action_id?from_day=-29&to_day=0

#### days endpoint query params:
- from_day: start day report, delta days from today, default: -29
- to_day: finish day report, delta days from today, default: 0
