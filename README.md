# Household Task Management

Runing migrations.

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