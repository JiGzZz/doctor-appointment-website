from flask import Flask, render_template, jsonify, request

from database import load_doctors_from_db, load_doctor_from_db, add_application_to_db

app = Flask(__name__)


@app.route("/")
def home():
  doctors = load_doctors_from_db()
  return render_template('home.html', doctors=doctors)


@app.route("/api/doctors")
def get_doctors():
  doctors = load_doctors_from_db()
  return jsonify(doctors)


@app.route("/doctor/<id>")
def show_doctor(id):
  doctor = load_doctor_from_db(id)

  if not doctor:
    return "Not Found", 404

  return render_template('doctorpage.html', doctor=doctor)


@app.route("/doctor/<id>/book", methods=['post'])
def book_doctor(id):
  data = request.form
  doctor = load_doctor_from_db(id)
  add_application_to_db(id, data)
  return render_template('application_submitted.html',
                         application=data,
                         doctor=doctor)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
