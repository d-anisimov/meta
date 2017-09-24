import flask
from flask import request, abort, jsonify

from sched_meta.db import db_session
from sched_meta.models import User, Group

bp = flask.Blueprint("groups_endpoints", __name__)


@bp.route("/create", methods=["PUT"])
def create():
    admin_id = request.form["admin_id"]
    admin = db_session.query(User).get(admin_id)

    if not admin:
        abort(422, "Unknown admin_id")

    title = request.form["title"]

    group = Group(admin, title)
    db_session.add(group)
    db_session.commit()

    return jsonify(group.as_json())
