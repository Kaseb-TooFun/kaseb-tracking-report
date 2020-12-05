# Kaseb Tracking Report APIs

### Requirements:

- Python (3.8.6)
- virtualenv
- Python libraries in [requirements.txt](requirements.txt)

### Run server
1. Create virtual env for python libraries & activate it:
    - `virtualenv -p python3.8.6 venv`
    - `source venv/bin/activate`
 
2. Install required libraries:
    - `pip install -r requirements.txt`
    
3. Set required environment variables:
    - Copy [sample_env.sh](sample_env.sh) to `env.sh`: `cp sample_env.sh env.sh`
    - Fill `env.sh` by your environment values
    - `source env.sh`
    
4. `python manage.py runserver`

5. Enjoy.


---

# Endpoints
- /api/report/total/website/{website_id}
- /api/report/total/website/{website_id}/action/{action_id}
- /api/report/days/website/{website_id}?from_day=20201201&to_day=20201213
- /api/report/days/website/{website_id}/action/{action_id}?from_day=20201201&to_day=20201213

#### headers:
- Authorization:
    1. admin_key 
    2. or valid authorization header in kaseb backend


#### unique session option in all report endpoints
- Add `distinct=true` to url params.


#### days endpoint query params:
Key  |  Description |  Format  |  Default
---|---|---|---
from_day | start day of report | `YYYYmmdd` | 29 days ago
to_day | finish day of report | `YYYYmmdd` | today


#### Result Sample
1. Total
```json
{
   "websiteId" : "your-website-id",
   "total" : {
      "clickedCount" : 0,
      "closedCount" : 9,
      "conversionRate" : 0,
      "desktopToAllPercent" : 70,
      "executeCount" : 38,
      "pageViewCount" : 0
   }
}
```

2. Days
```json
{
   "websiteId" : "your-website-id",
   "days" : [
      {
         "clickedCount" : 0,
         "closedCount" : 0,
         "conversionRate" : 0,
         "day" : "2020/12/03",
         "executeCount" : 0,
         "pageViewCount" : 0
      },
      {
         "clickedCount" : 0,
         "closedCount" : 0,
         "conversionRate" : 0,
         "day" : "2020/12/04",
         "executeCount" : 0,
         "pageViewCount" : 0
      }
   ]
}

```

---
