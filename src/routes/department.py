from flask import Blueprint, jsonify

from database.db import Database
from models.department import Department

main = Blueprint("department_blueprint", __name__)


@main.route("/get/<int:dept_id>", methods=["GET"])
def get_department(dept_id):
    db = Database.get_instance()
    with db.get_session() as session:
        department = session.query(Department).get(dept_id)
        if department:
            return jsonify(department.to_dict()), 200
        else:
            return jsonify({'message': "User not found"}), 404
