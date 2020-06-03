# Household Task Management
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/MLH-Fellowship/0.5.1-household.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MLH-Fellowship/0.5.1-household/context:python) [![Total alerts](https://img.shields.io/lgtm/alerts/g/MLH-Fellowship/0.5.1-household.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MLH-Fellowship/0.5.1-household/alerts/)

## Structure
Push only stuff ready to go to the `master` branch – it will be automatically deployed to Heroku.

## Runing migrations.

## Setting up development environment
 1. Set up virtual environment
```
python3 -m venv venv
```
 2. Install requirements
```
pip install -r requirements.txt
```
If it fails – remove psycopg2 from requirements.txt

3. Set `DATABASE_URL` environment variable (otherwise it will use SQLite – this works)
```
export DATABASE_URL=<some SQL URI>
```

4. Run migrations
```
flask db upgrade
```
