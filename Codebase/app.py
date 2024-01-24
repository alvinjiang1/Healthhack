import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from google.cloud import vision
from sqlalchemy.sql import text
from datetime import datetime

db = SQLAlchemy()

app = Flask(__name__)

# Initialize Database
db_name = 'healthhack.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# initialize the app with Flask-SQLAlchemy
db.init_app(app)

# Initialize Tables within SLQAlchemy
class MedicalReport(db.Model):
    __tablename__ = 'medical_report'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.now(tz=None))

# Route to insert a new user
@app.route('/add_report', methods=['POST'])
def add_report():
    if request.method == 'POST':
        # Get username and email from the request data                
        date_created = datetime.now() 
        filename = request.form.get("filename")       
        # Create a new user instance
        new_report = MedicalReport(filename=filename, date_created=date_created)

        # Add the new user to the database
        db.session.add(new_report)
        db.session.commit()

        return 'Medical Report added successfully!'
    else:
        return 'Invalid request method'

passkey = "/Users/alvin/Desktop/Healthhack/team-fath-f9cf4023f0e5.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = passkey
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/db_test')
def db_test():
    return render_template('db_test.html')
def index():
    return render_template('index.html')

"""Detects text in the file."""    
@app.route('/detect', methods=['POST'])
def detect_text(path):    
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        print(f'\n"{text.description}"')        

        # vertices for bounding boxes (NOT USED YET)
        # vertices = [
        #     f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
        # ]

        # print("bounds: {}".format(",".join(vertices)))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    result = ""
    for text in texts:
        result = text.description
        break
    return result

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')
    
    # Create the uploads folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Save the file to the uploads folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Use Google Cloud Vision API to extract text from the image
    texts = detect_text(file_path)

    if not texts:
        result = 'No text found in the image.'
    else:
        result = texts

    return render_template('index.html', result=result)

# this route will test the database connection - and nothing more
@app.route('/db')
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

if __name__ == '__main__':
    app.run(debug=True)
