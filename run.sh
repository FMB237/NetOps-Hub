# This the file used to run the program withput any path errors from the app 

# PYTHONPATH=/home/bruce/NetOps-Hub uvicorn main:app --reload

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 &