from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_doctors_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from doctors"))
    jobs = []
    for row in result.all():
      jobs.append(row._asdict())
    return jobs


def load_doctor_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text(f"SELECT * FROM doctors WHERE id = {id}"))
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return rows[0]._asdict()


def add_application_to_db(doctor_id, data):
  with engine.connect() as conn:
    query = text(
      "INSERT INTO applications (doctor_id, first_name, last_name, email, dob, gender, phone_number, appointment_date, time_slot) VALUES (:doctor_id, :first_name, :last_name, :email, :dob, :gender, :phone_number, :appointment_date, :time_slot)"
    )

    conn.execute(query,
                 doctor_id=doctor_id,
                 first_name=data['first_name'],
                 last_name=data['last_name'],
                 email=data['email'],
                 dob=data['dob'],
                 gender=data['gender'],
                 phone_number=data['phone_number'],
                 appointment_date=data['appointment_date'],
                 time_slot=data['time_slot'])
