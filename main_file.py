import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai
import time

openai.api_key = 'your_openai_api_key'


def generate_quiz(question_number):
    # It is an example prompt.
    prompt = f"""
    Generate a detailed quiz question for the NEET PG 2024 Anatomy syllabus at a moderate difficulty level, including which option (A, B, C, or D) is correct. This is question number {question_number} of 25. Provide a question with 4 options where one is correct, and give an explanation for why the correct option is right.

    Format the response as:
    Title: <Unique Title>
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


    response_text = response['choices'][0]['text'].strip()
    response_lines = response_text.split('\n')
    response_dict = {line.split(': ')[0]: line.split(': ')[1] for line in response_lines if ': ' in line}


    required_keys = ['Title', 'Question', 'A', 'B', 'C', 'D', 'Correct', 'ReasonA', 'ReasonB', 'ReasonC', 'ReasonD', 'Description']
    for key in required_keys:
        if key not in response_dict:
            response_dict[key] = ''

    sheet_data = ["" for _ in range(14)]
    column_map = {
        'Title': 0,
        'Question': 1,
        'A': 3,
        'B': 4,
        'C': 5,
        'D': 6,
        'Correct': 7,
        'ReasonA': 8,
        'ReasonB': 9,
        'ReasonC': 10,
        'ReasonD': 11,
        'Description': 13
    }
    for key, index in column_map.items():
        sheet_data[index] = response_dict[key]

    return sheet_data

try:
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'your_path_to_credentials_file',
        scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    )
except Exception as e:
    print(f"Error loading credentials: {e}")
    exit(1)

client = gspread.authorize(credentials)
sheet = client.open('your_google_sheet_name').sheet1

total_questions = int(input("enter no. of questions: "))
sleep_duration_in_seconds = 20

for question_number in range(1, total_questions + 1):
    next_row = len(sheet.get_all_values()) + 1
    quiz_data = generate_quiz(question_number)
    sheet.insert_row(quiz_data, next_row)
    print(f"Quiz question and details added to Google Sheet at row {next_row}: {quiz_data}")
    time.sleep(sleep_duration_in_seconds)

print("All questions have been successfully added.")