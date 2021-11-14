import os, secrets
from flask import current_app as app
from flask import render_template, redirect, url_for, send_from_directory, flash
from .forms import form_post
from .db import db_post, db_get, db_update_thread
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .image import upload_image
from datetime import datetime

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/')
def index():
    form = form_post()

    threads = []
    replies = []

    for thread in db_get(False, False, 'thread'):
        threads.append(thread)

    for reply in db_get(False, False, 'reply'):
        replies.append(reply)

    return render_template('index.html', threads=threads, replies=replies, form=form)

@app.route('/thread/<thread_id>')
def thread(thread_id):
    form = form_post()

    threads = []
    replies = []

    for thread in db_get(thread_id, False, 'thread'):
        threads.append(thread)

    for reply in db_get(thread_id, False, 'reply'):
        replies.append(reply)
    
    if threads:
        return render_template('thread.html', threads=threads, replies=replies, form=form)
    else:
        flash('Oops.. something went wrong', 'warning')
        return redirect(url_for('index'))


@app.route('/thread', methods=['POST'])
@limiter.limit("1/second", override_defaults=False)
def post_thread():
    form = form_post()

    if form.validate_on_submit():
        if form.upload.data:
            url = upload_image(form.upload.data)
        else:
            url = None
        
        thread_id = str(secrets.token_urlsafe(8))
        post_id = str(secrets.token_urlsafe(6))
        last_update = datetime.utcnow()

        semchan_table = db_post('thread', thread_id, post_id, form.title.data, form.body.data, url)
        semchan_table.add_row()

        db_update_thread(thread_id, post_id, last_update)

    return redirect(url_for('index'))

@app.route('/reply/<thread_id>', methods=['POST'])
@limiter.limit("1/second", override_defaults=False)
def post_reply(thread_id):
    form = form_post()

    if form.validate_on_submit():
        if form.upload.data:
            url = upload_image(form.upload.data)
        else:
            url = None

        semchan_table = db_post('reply', str(thread_id), str(secrets.token_urlsafe(6)), form.title.data, form.body.data, url)
        semchan_table.add_row()

        thread = list(db_get(thread_id, False, 'thread'))
        post_id = thread[0].RowKey

        #might not even have to add a last_update as the native 'Timestamp' gets updated when the item gets updated
        #would be better to record amount of replies instead to have some updating mechanism for the thread so we use it to sort updated threads first
        #recording two timestamps is not smart but it does what we want for now
        last_update = datetime.utcnow()
        db_update_thread(thread_id, post_id, last_update)

    return redirect(url_for('thread', thread_id=thread_id))

@app.route('/favicon.ico')
def favicon():
    path = os.path.join(app.root_path, 'static/')
    print(path)
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def page_not_found(e):
    flash('Oops.. something went wrong', 'warning')
    return redirect(url_for('index'))

@app.errorhandler(400)
def page_not_found(e):
    flash('Sorry, that\'s not allowed', 'warning')
    return redirect(url_for('index'))