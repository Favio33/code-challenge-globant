from flask import jsonify
from sqlalchemy.dialects.postgresql import insert


def bulk_upsert(db_instance, model, request):

    data = request.get_json()

    # Verify json content
    if not isinstance(data, list):
        return jsonify({"error": "Se espera una lista de objetos"}), 400

    # Ensure every payload has an id
    if not all("id" in item for item in data):
        return jsonify({"error": "Todos los registros deben tener un ID"}), 400

    allowed_fields = set(model.__table__.columns.keys())

    sanitized_data = [{k: v for k, v in item.items() if k in allowed_fields} for item in data]

    insert_stmt = insert(model).values(sanitized_data)

    # Campos a actualizar (todos menos el ID)
    update_fields = {key: insert_stmt.excluded[key] for key in allowed_fields if key != "id"}

    upsert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=["id"],  # clave para detectar conflictos
        set_=update_fields,
    )

    with db_instance.get_session() as session:
        try:
            session.execute(upsert_stmt)
            session.commit()
            return jsonify(
                {"message": f"{len(sanitized_data)} registros insertados/actualizados"}
            ), 200
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
