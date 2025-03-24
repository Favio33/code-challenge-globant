from flask import Blueprint, jsonify, request

from database.db import Database
from models.hired_employees import HiredEmployees
from utils.bulk import bulk_upsert
from utils.csv_loader import insert_historical_csv
from utils.update import update_id

employees_bp = Blueprint("employees_blueprint", __name__)


@employees_bp.route("/get/<int:employee_id>", methods=["GET"])
def get_department(employee_id):
    db = Database.get_instance()
    with db.get_session() as session:
        employee = session.query(HiredEmployees).get(employee_id)
        if employee:
            return jsonify(employee.to_dict()), 200
        else:
            return jsonify({'message': "Employee not found"}), 404

@employees_bp.route("/update", methods=["PUT"])
def update_job():
    db = Database.get_instance()
    return update_id(db, HiredEmployees, request)

@employees_bp.route("/bulk", methods=["POST"])
def bulk_upsert_job():
    db = Database.get_instance()
    return bulk_upsert(db, HiredEmployees, request)

@employees_bp.route('/upload-historical', methods=['POST'])
def upload_csv():
    file = request.files.get('file')
    has_header = eval(request.args.get("has_header"))
    batch_size = int(request.args.get("batch_size")) if request.args.get("batch_size") else 1000 
    csv_headers =  None if has_header else [col.strip().lower() for col in request.args.get("csv_schema").split(',')]
    db = Database.get_instance()
    return insert_historical_csv(file, HiredEmployees, db, batch_size, has_header, csv_headers)
