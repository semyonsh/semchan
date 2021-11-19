# semchan

A very simple Flask imageboard powered by Azure Storage Account + Azure Table Storage 
![image](https://user-images.githubusercontent.com/3471635/142597608-9f7102d5-7630-49a8-89a8-3a8bc493f168.png)


## set-up
```bash
pip install -r requirements.txt
```

Create an .env file in root folder (Or load environment variables in the way of choosing, i use decouple for this atm), and fill it with the credentials for the storage account, a random secret key for CSRF tokens and a prefix URL for the storage account or CNAME applied:
```
AZURE_STORAGE_ACCOUNT_NAME=
AZURE_STORAGE_ACCOUNT_KEY=
AZURE_STORAGE_CONNECTION_STRING=
AZURE_TABLE_STORAGE_NAME=semchan
IMAGE_URL=https://image.website/
```

Run with ```run.sh``` if using ```gunicorn``` or set ```FLASK_APP=application\__init__.py``` in environment and use ```flask run```.

OR

Run with docker:

```docker build -t semchan .```

```docker run -p 8000:8000 --env-file .\.env semchan```
