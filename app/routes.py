from flask import render_template, request, jsonify, abort, g
from flask_cas import login_required
from app import app, db, tasks, cas
from app.models import User
from app.cas_validate import validate
from sqlalchemy import distinct

import datetime
import time


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.before_request
def store_user():
    if request.method != 'OPTIONS':
        if cas.username:
            g.user = User.query.get(cas.username)
            timestamp = int(time.time())
            if not g.user:
                g.user = User(username=cas.username,
                              registered_on=timestamp)
                db.session.add(g.user)
            g.user.last_seen = timestamp
            db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/apidocs')
def apidocs():
    return render_template('apidocs.html')


@app.route('/token', methods=['POST'])
def get_token():
    token, expires_in = g.user.generate_token()
    return jsonify({'token': token, 'expires_in': expires_in})
