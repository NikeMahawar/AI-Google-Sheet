from flask import Flask, request, render_template, jsonify
import main
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('create_form.html')

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    audience = request.form['peopleType']
    subject = request.form['subject']
    topic = request.form['topic']
    difficulty = request.form['difficulty']
    num_questions = int(request.form['numQuestions'])
    grade = request.form.get('grade')
    college_course = request.form.get('collegeCourse')

    pyq_file = request.files['pyqFile']
    pyq_text = None
    if pyq_file and allowed_file(pyq_file.filename):
        pyq_text = extract_text_from_pdf(pyq_file)

    response = main.generate_and_add_questions(
        audience=audience,
        number_of_questions=num_questions,
        subject=subject,
        topic=topic,
        difficulty=difficulty,
        grade=grade,
        college_course=college_course,
        pyq_text=pyq_text
    )

    return jsonify({"message": response})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf']

def extract_text_from_pdf(file_stream):
    reader = PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

if __name__ == "__main__":
    app.run(debug=True)
