from flask import Blueprint, jsonify, request

from database.db import Database
from models.jobs import Jobs
from utils.bulk import bulk_upsert
from utils.update import update_id

main = Blueprint("job_blueprint", __name__)


@main.route("/get/<int:job_id>", methods=["GET"])
def get_department(job_id):
    db = Database.get_instance()
    with db.get_session() as session:
        job = session.query(Jobs).get(job_id)
        if job:
            return jsonify(job.to_dict()), 200
        else:
            return jsonify({"message": "Job not found"}), 404

@main.route("/update", methods=["PUT"])
def update_job():
    db = Database.get_instance()
    return update_id(db, Jobs, request)

@main.route("/bulk", methods=["POST"])
def bulk_upsert_job():
    db = Database.get_instance()
    return bulk_upsert(db, Jobs, request)
