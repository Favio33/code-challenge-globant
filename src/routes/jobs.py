from flask import Blueprint, jsonify

from database.db import Database
from models.jobs import Jobs

main = Blueprint("job_blueprint", __name__)


@main.route("/get/<int:job_id>", methods=["GET"])
def get_department(job_id):
    db = Database.get_instance()
    with db.get_session() as session:
        job = session.query(Jobs).get(job_id)
        if job:
            return jsonify(job.to_dict()), 200
        else:
            return jsonify({'message': "Job not found"}), 404
