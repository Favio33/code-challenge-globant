from flask import jsonify
from sqlalchemy import func


def update_id(db_instance, model, request):
    id = request.args.get("id")
    with db_instance.get_session() as session:
        id_to_update = session.query(model).get(id)

        if not id_to_update:
            return jsonify({"message": "User not found"}), 404

        allowed_fields = set(model.__table__.columns.keys()) - {"id"}
        data = request.get_json()

        for key in data.keys():
            if key in allowed_fields:
                setattr(id_to_update, key, data[key])

        id_to_update.last_updated = func.now()

        try:
            session.commit()
            return jsonify(id_to_update.to_dict()), 200
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500