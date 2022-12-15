# Run the API endpoint inside the docker
uwsgi --ini uwsgi.ini &

# Run a script that sends POST to backend every few seconds
python scheduler.py
