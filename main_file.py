import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai
import time
import uuid

openai.api_key = 'Set-Your-Own-API-KEY'

def generate_quiz(question_number, audience, subject, topic, difficulty, grade=None, college_course=None):
    required_keys = ['Question', 'A', 'B', 'C', 'D', 'Correct', 'ReasonA', 'ReasonB', 'ReasonC', 'ReasonD', 'Description']
    audience_details = {
        "school_students": f"for grade {grade} students",
        "college": f"in the {college_course} course",
        "custom": "for a custom audience"
    }.get(audience, "for a general audience")
    while True:
        prompt = f"""
            Generate a quiz question {audience_details} on the topic of {topic} in {subject} at a {difficulty} difficulty level. This is question number {question_number}. Provide a question with 4 options where one is correct, and give an explanation for why the correct option is right.

            Format the response as:
            Question: <Question Text>
            A: <Option A>
            B: <Option B>
            C: <Option C>
            D: <Option D>
            Correct: <Correct option among A, B, C, or D>
            ReasonA: <Explanation for A>
            ReasonB: <Explanation for B>
            ReasonC: <Explanation for C>
            ReasonD: <Explanation for D>
            Description: <Any additional information or description related to the question>
            """
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                temperature=0.5,
                max_tokens=1024,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["\n\n"]
            )
        except openai.error.RateLimitError:
            print("Rate limit reached. Waiting for 60 seconds before retrying...")
            time.sleep(60)
            continue

        response_text = response['choices'][0]['text'].strip()
        response_lines = response_text.split('\n')
        response_dict = {line.split(': ')[0]: line.split(': ')[1] for line in response_lines if ': ' in line}


        question_id = str(uuid.uuid4())
        response_dict['ID'] = question_id

        response_dict['Image'] = 'add_your_own_image'

        if all(key in response_dict for key in required_keys):
            break

    return [response_dict.get(key, '') for key in required_keys + ['ID', 'Image']]

def generate_and_add_questions(audience, number_of_questions, subject, topic, difficulty, grade=None, college_course=None, pyq_text=None):

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'Replace with your JSON keyfile path',
        scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open('your_own_google_sheet_name')


    sheet_title = subject

    try:
        sheet = spreadsheet.worksheet(sheet_title)
    except gspread.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title=sheet_title, rows=str(number_of_questions + 1), cols="20")

    for question_number in range(1, number_of_questions + 1):
        quiz_data = generate_quiz(question_number, audience, subject, topic, difficulty, grade, college_course)
        quiz_data = [str(question_number)] + quiz_data + [""]

        next_row = len(sheet.get_all_values()) + 1
        sheet.insert_row(quiz_data, next_row)
        print(f"Question {question_number}/{number_of_questions} added to the {sheet_title} sheet at row {next_row}.")
        time.sleep(20)
    return f"All {number_of_questions} questions have been successfully added to the {sheet_title} Google Sheet."
