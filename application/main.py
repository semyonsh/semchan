import os
import secrets
from datetime import datetime

from flask import current_app as app
from flask import render_template, redirect, url_for, send_from_directory, flash, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .db import dbPost, db_get, db_update_thread
from .forms import formPost
from .image import upload_image


limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


@app.route('/')
def index():
    form = formPost()

    threads = []
    all_replies = []

    for thread in db_get(False, False, 'thread'):
        threads.append(thread)

    for reply in db_get(False, False, 'reply'):
        all_replies.append(reply)


    return render_template('index.html', threads=threads, all_replies=all_replies, form=form)


@app.route('/thread/<thread_id>')
def thread(thread_id):
    form = formPost()

    threads = []
    replies = []

    for thread in db_get(thread_id, False, 'thread'):
        threads.append(thread)

    for reply in db_get(thread_id, False, 'reply'):
        replies.append(reply)

    post_id = request.args.get('reply', None)
    if post_id:
        form.body.data = '>' + post_id + '\n'

    if threads:
        return render_template('thread.html', threads=threads, post_id=post_id, replies=replies, form=form)
    else:
        flash('Oops.. something went wrong', 'warning')
        return redirect(url_for('index'))


@app.route('/thread', methods=['POST'])
@limiter.limit("1/second", override_defaults=False)
def post_thread():
    form = formPost()
    url = None
    thumb_url = None

    if form.validate_on_submit():
        if form.upload.data:
            get_url = upload_image(form.upload.data)
            if get_url[0]:
                url = get_url[0]
            if get_url[1]:
                thumb_url = get_url[1]

        thread_id = str(secrets.token_urlsafe(6))
        post_id = str(secrets.token_urlsafe(6))
        time_created = datetime.utcnow()

        # noinspection SpellCheckingInspection
        semchan_table = dbPost('thread', thread_id, post_id, form.title.data, form.body.data, url, thumb_url, time_created, 0)
        semchan_table.add_row()

    return redirect(url_for('index'))



@app.route('/reply/<thread_id>', methods=['POST'])
@limiter.limit("1/second", override_defaults=False)
def post_reply(thread_id):
    form = formPost()
    url = None
    thumb_url = None

    if form.validate_on_submit():
        if form.upload.data:
            get_url = upload_image(form.upload.data)
            if get_url[0]:
                url = get_url[0]
            if get_url[1]:
                thumb_url = get_url[1]


        time_created = datetime.utcnow()


        semchan_table = dbPost('reply', str(thread_id), str(secrets.token_urlsafe(6)), form.title.data, form.body.data,
                               url, thumb_url, time_created, 0)
        semchan_table.add_row()

        thread = list(db_get(thread_id, False, 'thread'))
        post_id = thread[0].RowKey

        reply_count = int(thread[0].reply_count) + 1
        db_update_thread(thread_id, post_id, reply_count)

    return redirect(url_for('thread', thread_id=thread_id))


@app.route('/favicon.ico')
def favicon():
    path = os.path.join(app.root_path, 'static/')
    print(path)
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def page_not_found(e):
    flash('Oops.. something went wrong', 'info')
    return redirect(url_for('index'))


@app.errorhandler(400)
def page_not_found(e):
    flash('Sorry, that\'s not allowed', 'danger')
    return redirect(url_for('index'))

@app.errorhandler(413)
def page_not_found(e):
    flash('File is larger than 5MB', 'warning')
    return redirect(url_for('index'))

