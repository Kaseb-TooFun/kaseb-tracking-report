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

### Endpoints
- /api/report/total/website/website_id
- /api/report/total/website/website_id/action/action_id
- /api/report/days/website/website_id?from_day=-29&to_day=0
- /api/report/days/website/website_id/action/action_id?from_day=-29&to_day=0

#### headers:
- Authorization:
    1. admin_key 
    2. or valid authorization header in kaseb backend

#### days endpoint query params:
- from_day: start day report, delta days from today, default: -29
- to_day: finish day report, delta days from today, default: 0


---
