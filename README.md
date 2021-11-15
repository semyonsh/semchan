# semchan

A Flask imageboard (in progress) powered by Azure Storage Account + Azure Table Storage 
![image](https://user-images.githubusercontent.com/3471635/141687976-dbc1fc68-a531-45a8-9e37-e703d9205827.png)

## set-up
```bash
pip install -r requirements.txt


#requirements.txt
flask
azure-storage-blob
azure-cosmosdb-table
Flask-WTF
flask-bootstrap
Flask-Limiter
python-decouple
```

Create an .env file in ```application\``` (Or load environment variables in the way of choosing, i use decouple for this atm), and fill it with the credentials for the storage account, a random secret key for CSRF tokens and a prefix URL for the storage account or CNAME applied:
```
AZURE_STORAGE_ACCOUNT_NAME=
AZURE_STORAGE_ACCOUNT_KEY=
AZURE_STORAGE_CONNECTION_STRING=
SECRET_KEY=changeme
IMAGE_URL=https://image.website/
```

Run with ```run.sh``` if using ```gunicorn3``` or set ```FLASK_APP=application\__init__.py``` in environment and use ```flask run```. 

## todo

- get rid of [this](https://github.com/semyonsh/semchan/blob/c1f19d8587b4d3f99d47b0eb585eb5133cf55959/application/main.py#L91), replace it with something meaningful
- pagination and/or remove threads if above threshold of age/amount of threads
- dont show all replies on front page
- urlize thread and post ids
- special formatting for quotes like > etc. 
- stylize things like replies not having full width
- make validation more robust
