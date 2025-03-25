from flask import Blueprint, jsonify, request

from database.db import Database
from models.jobs import Jobs
from utils.bulk import bulk_upsert
from utils.csv_loader import insert_historical_csv
from utils.update import update_id

jobs_bp = Blueprint("job_blueprint", __name__)


@jobs_bp.route("/get/<int:job_id>", methods=["GET"])
def get_department(job_id):
    db = Database.get_instance()
    with db.get_session() as session:
        job = session.query(Jobs).get(job_id)
        if job:
            return jsonify(job.to_dict()), 200
        else:
            return jsonify({"message": "Job not found"}), 404

@jobs_bp.route("/update", methods=["PUT"])
def update_job():
    db = Database.get_instance()
    return update_id(db, Jobs, request)

@jobs_bp.route("/bulk", methods=["POST"])
def bulk_upsert_job():
    db = Database.get_instance()
    return bulk_upsert(db, Jobs, request)

@jobs_bp.route('/upload-historical', methods=['POST'])
def upload_csv():
    db = Database.get_instance()
    return insert_historical_csv(Jobs, db, request)
