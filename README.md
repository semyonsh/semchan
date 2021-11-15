# semchan

A Flask imageboard (in progress) powered by Azure Storage Account + Azure Table Storage 
![image](https://user-images.githubusercontent.com/3471635/141687976-dbc1fc68-a531-45a8-9e37-e703d9205827.png)

## set-up
```bash
pip install -r requirements.txt
```

Create an .env file in root folder (Or load environment variables in the way of choosing, i use decouple for this atm), and fill it with the credentials for the storage account, a random secret key for CSRF tokens and a prefix URL for the storage account or CNAME applied:
```
AZURE_STORAGE_ACCOUNT_NAME=
AZURE_STORAGE_ACCOUNT_KEY=
AZURE_STORAGE_CONNECTION_STRING=
SECRET_KEY=changeme
IMAGE_URL=https://image.website/
```

Run with ```run.sh``` if using ```gunicorn``` or set ```FLASK_APP=application\__init__.py``` in environment and use ```flask run```.

OR

Run with docker:

```docker build -t semchan .```

```docker run -p 8000:8000 --env-file .\.env semchan```


## todo

- pagination and/or remove threads if above threshold of age/amount of threads
- dont show all replies on front page
- urlize thread and post ids
- special formatting for quotes like > etc. 
- stylize things like replies not having full width
