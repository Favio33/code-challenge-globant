from flask import Blueprint, jsonify

from database.db import Database
from models.hired_employees import HiredEmployees

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
