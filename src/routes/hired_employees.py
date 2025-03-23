from flask import Blueprint, jsonify, request

from database.db import Database
from models.hired_employees import HiredEmployees
from utils.bulk import bulk_upsert
from utils.update import update_id

main = Blueprint("employees_blueprint", __name__)


@main.route("/get/<int:employee_id>", methods=["GET"])
def get_department(employee_id):
    db = Database.get_instance()
    with db.get_session() as session:
        employee = session.query(HiredEmployees).get(employee_id)
        if employee:
            return jsonify(employee.to_dict()), 200
        else:
            return jsonify({'message': "Employee not found"}), 404

@main.route("/update", methods=["PUT"])
def update_job():
    db = Database.get_instance()
    return update_id(db, HiredEmployees, request)

@main.route("/bulk", methods=["POST"])
def bulk_upsert_job():
    db = Database.get_instance()
    data = request.get_json()
    return bulk_upsert(db, HiredEmployees, data)
