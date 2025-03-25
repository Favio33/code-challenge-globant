import numpy as np
import pandas as pd


def insert_historical_csv(model,
                          db_instance,
                          request):
    file = request.files.get('file')
    has_header = request.args.get("has_header", "true").lower() == "true"
    batch_size = int(request.args.get("batch_size", 1000))
    csv_schema = request.args.get("csv_schema", "").strip()
    columns = None if has_header else [col.strip().lower() for col in csv_schema.split(',')] if csv_schema else None

    allowed_columns = set(model.__table__.columns.keys())

    if not file or not file.filename.endswith('.csv'):
        return {"error": "Invalid file format. Please upload a CSV file."}, 400

    with db_instance.get_session() as session:
        try:
            if has_header:
                df = pd.read_csv(file)
            else:
                if not columns:
                    return {"error": "Columns must be provided if CSV has no header"}
                df = pd.read_csv(file, header=None)
                df.columns = columns

            if allowed_columns:
                df = df[[col for col in df.columns if col in allowed_columns]]
                df = df.replace(np.nan, None)

            records = df.to_dict(orient='records')

            batch = []
            for record in records:
                instance = model(**record)
                batch.append(instance)

                if len(batch) >= batch_size:
                    session.add_all(batch)
                    session.commit()
                    batch = []

            if batch:
                session.add_all(batch)
                session.commit()

            return {"message": f"{len(records)} records inserted successfully"}

        except Exception as e:
            session.rollback()
            return {"error": f"Failed to insert data: {str(e)}"}
