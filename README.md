#semchan

A Flask imageboard (in progress) powered by Azure Storage Account + Azure Table Storage 

##set-up
```bash
#Create a venv if you want to
python -m venv venv
#Install modules
pip install -r requirements.txt
```

Create a .env file in ```application\``` (Or load environment variables in the way of choosing), and fill it with the credentials for the storage account, a secret key for CSRF tokens and a prefix URL for the storage account or CNAME applied:
```
AZURE_STORAGE_ACCOUNT_NAME=
AZURE_STORAGE_ACCOUNT_KEY=
AZURE_STORAGE_CONNECTION_STRING=
SECRET_KEY=
IMAGE_URL=https://image.website/
```

Run with ```run.sh``` if using ```gunicorn3``` or set ```FLASK_APP=application\__init__.py``` in environment.