release: flask db upgrade
web: gunicorn --worker-class eventlet -w 1 app:'create_app()'
worker: ./target/release/worker
