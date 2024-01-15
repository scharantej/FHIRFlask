 
# Import necessary libraries
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Create a Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fhir.db'
db = SQLAlchemy(app)

# Define the Patient model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)

# Define the Observation model
class Observation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    value = db.Column(db.Float)

# Create the database tables
db.create_all()

# Define the routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fhir/Patient')
def get_patients():
    patients = Patient.query.all()
    return jsonify([patient.to_dict() for patient in patients])

@app.route('/fhir/Patient/<patient_id>')
def get_patient(patient_id):
    patient = Patient.query.get(patient_id)
    return jsonify(patient.to_dict())

@app.route('/fhir/Observation')
def get_observations():
    observations = Observation.query.all()
    return jsonify([observation.to_dict() for observation in observations])

@app.route('/fhir/Observation/<observation_id>')
def get_observation(observation_id):
    observation = Observation.query.get(observation_id)
    return jsonify(observation.to_dict())

# Run the app
if __name__ == '__main__':
    app.run()
