web: flask db upgrade;  gunicorn --worker-class eventlet -w 1 app:'create_app()'
worker: python worker.py
