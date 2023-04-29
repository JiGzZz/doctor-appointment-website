from sqlalchemy import create_engine, text

import os
from datetime import datetime

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_doctors_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from doctors"))
    doctors = []
    for row in result.all():
      doctors.append(row._asdict())
    return doctors


def load_doctor_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text(f"SELECT * FROM doctors WHERE id = {id}"))
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return rows[0]._asdict()


def add_application_to_db(id, data):
  # print(id)
  # sys.exit(0)
  with engine.connect() as conn:
    query = text(
      "INSERT INTO appointments (doctor_id, first_name, last_name, email, age, gender, phone_number, app_date, time_slot) VALUES (:doctor_id, :first_name, :last_name, :email, :age, :gender, :phone_number, :app_date, :time_slot)"
    )

    app_date = datetime.strptime(data['app_date'], '%d/%m/%Y')

    conn.execute(
      query, {
        "doctor_id": id,
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "email": data['email'],
        "age": data['age'],
        "gender": data['gender'],
        "phone_number": data['phone_number'],
        "app_date": app_date.strftime('%Y-%m-%d'),
        "time_slot": data['time_slot']
      })
    # conn.execute(text(INSERT INTO applications (doctor_id, first_name, last_name, email, age, gender, phone_number, app_date, time_slot) VALUES ({id}, {data['first_name']}, {data['last_name']}, {data['email']}, {data['age']}, {data['gender']}, {data['phone_number']}, {data['app_date']}, {data['time_slot']}))
