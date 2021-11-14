from decouple import config
from azure.cosmosdb.table.models import Entity
from azure.cosmosdb.table.tableservice import TableService

account_name = config('AZURE_STORAGE_ACCOUNT_NAME')
account_key = config('AZURE_STORAGE_ACCOUNT_KEY')

connect_db = TableService(account_name=account_name, account_key=account_key)
usr_post = Entity()

class db_post:
    def __init__(self, post_type, thread_id, post_id, title, body, url):
        self.post_type = post_type
        self.thread_id = thread_id
        self.post_id = post_id
        self.title = title
        self.body = body
        self.url = url

    def add_row(self):
        usr_post.PartitionKey = self.thread_id
        usr_post.RowKey = self.post_id
        usr_post.post_type = self.post_type
        usr_post.title = self.title
        usr_post.body = self.body
        usr_post.url = self.url

        connect_db.insert_entity('semchan', usr_post)

#we don't use the post_id yet in queries but could be useful in the future
def db_get(thread_id=False, post_id=False, post_type=False):
    if thread_id == False and post_id == False and post_type == False:
        posts = connect_db.query_entities('semchan')
    elif thread_id and post_type:
        posts = connect_db.query_entities('semchan', filter="PartitionKey eq '" + thread_id + "' and post_type eq '" + post_type + "'")
    elif thread_id:
        posts = connect_db.query_entities('semchan', filter="PartitionKey eq '" + thread_id + "'")
    elif post_id:
        posts = connect_db.query_entities('semchan', filter="RowKey eq '" + post_id + "'")
    elif post_type:
        posts = connect_db.query_entities('semchan', filter="post_type eq '" + post_type + "'")
    return posts

def db_update_thread(thread_id, post_id, last_update):
    thread = {'PartitionKey': thread_id, 
            'RowKey': post_id,
            'last_update': last_update}

    connect_db.merge_entity('semchan', thread)