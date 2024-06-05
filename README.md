# AI-Google-Sheet

## AI-Generated Quiz Question Uploader

This Python-Flask application automates the process of generating quiz questions with detailed options and correct answers using OpenAI's GPT-3.5 model. It integrates with Google Sheets to upload the generated quiz questions for easy management and sharing.

### Features

- **Automatic Question Generation**: Utilizes OpenAI's GPT-3.5 model to generate detailed quiz questions for a specified topic and difficulty level.
- **Multiple-Choice Options**: Includes four multiple-choice options (A, B, C, D) for each question, with one correct answer.
- **Explanations and Descriptions**: Provides explanations for each option and allows adding additional descriptions for better understanding.
- **Google Sheets Integration**: Uses the Google Sheets API to upload the generated quiz questions directly to a specified Google Sheet.
- **Customizable Parameters**: Users can customize the question generation prompt, API key, credentials file path, Google Sheet name, and the number of questions to generate.

### Usage

1. Set up the necessary API keys and credentials for OpenAI and Google Sheets.
2. Run the Flask application.
3. Access the web interface to specify the number of questions to generate and other parameters.
4. Upload a PDF file of previous year questions if needed.
5. The application will automatically generate and upload quiz questions with detailed options and correct answers to the specified Google Sheet.

### Requirements

- Python 3.x
- OpenAI API key
- Google Sheets API credentials JSON file
- Flask, gspread, PyPDF2, and oauth2client Python libraries

### Instructions

1. Install the required Python libraries using:
   ```sh
   pip install Flask gspread oauth2client PyPDF2
