from decouple import config
from azure.cosmosdb.table.models import Entity
from azure.cosmosdb.table.tableservice import TableService

account_name = config('AZURE_STORAGE_ACCOUNT_NAME')
account_key = config('AZURE_STORAGE_ACCOUNT_KEY')
table = config('AZURE_TABLE_STORAGE_NAME')

connect_db = TableService(account_name=account_name, account_key=account_key)
usr_post = Entity()


class dbPost:
    def __init__(self, post_type, thread_id, post_id, title, body, url, thumb_url, time_created=None, reply_count=0):
        self.post_type = post_type
        self.thread_id = thread_id
        self.post_id = post_id
        self.title = title
        self.body = body
        self.url = url
        self.thumb_url = thumb_url
        self.time_created = time_created
        self.reply_count = reply_count

    def add_row(self):
        usr_post.PartitionKey = self.thread_id
        usr_post.RowKey = self.post_id
        usr_post.post_type = self.post_type
        usr_post.title = self.title
        usr_post.body = self.body
        usr_post.url = self.url
        usr_post.thumb_url = self.thumb_url
        usr_post.time_created = self.time_created
        usr_post.reply_count = self.reply_count

        connect_db.insert_entity(table, usr_post)


# we don't use the post_id yet in queries but could be useful in the future
def db_get(thread_id, post_id, post_type):
    if thread_id is False and post_id is False and post_type is False:
        posts = connect_db.query_entities(table)
    elif thread_id and post_type:
        posts = connect_db.query_entities(table,
                                          filter="PartitionKey eq '" + thread_id + "' and post_type eq '" + post_type + "'")
    elif thread_id:
        posts = connect_db.query_entities(table, filter="PartitionKey eq '" + thread_id + "'")
    elif post_id:
        posts = connect_db.query_entities(table, filter="RowKey eq '" + post_id + "'")
    elif post_type:
        posts = connect_db.query_entities(table, filter="post_type eq '" + post_type + "'")
    return posts


def db_update_thread(thread_id, post_id, reply_count):
    thread = {'PartitionKey': thread_id,
              'RowKey': post_id,
              'reply_count': reply_count}

    connect_db.merge_entity(table, thread)
