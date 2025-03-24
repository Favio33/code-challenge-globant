import numpy as np
import pandas as pd


def insert_historical_csv(file,
                          model,
                          db_instance,
                          batch_size=1000,
                          has_header=True,
                          columns=None):

    allowed_columns = set(model.__table__.columns.keys())

    if not file or not file.filename.endswith('.csv'):
        return {"error": "Invalid file format. Please upload a CSV file."}

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
