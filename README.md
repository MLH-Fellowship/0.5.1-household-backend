# Household Task Management
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/MLH-Fellowship/0.5.1-household.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MLH-Fellowship/0.5.1-household/context:python) [![Total alerts](https://img.shields.io/lgtm/alerts/g/MLH-Fellowship/0.5.1-household.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MLH-Fellowship/0.5.1-household/alerts/)

## Structure
Push only stuff ready to go to the `master` branch – it will be automatically deployed to Heroku (only after the CI passes, though)!

## Runing migrations.

```
# 1. set up virtual environment
python3 -m venv venv
# 2. install requirements
pip install -r requirements.txt
# if it fails – remove psycopg2 from requirements.txt 
# 3. set `DATABASE_URL` environment variable (otherwise it will use SQLite – this works)
export DATABASE_URL=<some SQL URI>
# 4. run migrations
flask db upgrade
```
