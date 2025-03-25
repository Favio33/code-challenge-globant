from flask import Blueprint, jsonify, request

from database.db import Database
from models.department import Department
from utils.bulk import bulk_upsert
from utils.csv_loader import insert_historical_csv
from utils.update import update_id

department_bp = Blueprint("department_blueprint", __name__)


@department_bp.route("/get/<int:dept_id>", methods=["GET"])
def get_department(dept_id):
    db = Database.get_instance()
    with db.get_session() as session:
        department = session.query(Department).get(dept_id)
        if department:
            return jsonify(department.to_dict()), 200
        else:
            return jsonify({'message': "User not found"}), 404

@department_bp.route("/update", methods=["PUT"])
def update_job():
    db = Database.get_instance()
    return update_id(db, Department, request)

@department_bp.route("/bulk", methods=["POST"])
def bulk_upsert_job():
    db = Database.get_instance()
    return bulk_upsert(db, Department, request)

@department_bp.route('/upload-historical', methods=['POST'])
def upload_csv():
    db = Database.get_instance()
    return insert_historical_csv(Department, db, request)
