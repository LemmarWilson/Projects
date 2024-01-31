import os
import random
import smtplib

from openai import OpenAI
from email.message import EmailMessage
from openpyxl import load_workbook
from dotenv import load_dotenv


def tip_generator():
    # Load environment variables from a .env file
    load_dotenv()

    # Create the client object for the OpenAI API
    api_key = os.environ.get('OPENAI_API_KEY')
    chat_client = OpenAI(api_key=api_key)

    # Load the spreadsheet (Excel file) containing the topics and prompts
    workbook = load_workbook('./prompts.xlsx')
    sheet = workbook.active

    # Get the number of rows in the spreadsheet (excluding the header)
    num_rows = sheet.max_row - 1  # Subtract 1 for the header

    # Choose a random row number between 2 and the total number of rows
    random_row = random.randint(2, num_rows + 1)

    # Get the topic and prompt from the randomly selected row
    topic = sheet.cell(row=random_row, column=1).value
    prompt = sheet.cell(row=random_row, column=2).value

    # Use the OpenAI API to generate a response
    response = chat_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "{}".format(prompt)},
        ]
    )

    # Prepare the message to be sent
    message = "Topic: {}\n\n{}".format(topic, response.choices[0].message.content)
    return message


def send_text(body):
    # Load environment variables from a .env file
    user = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASSWORD')
    # to = os.environ.get('PHONE_NUMBER')
    to = 'lemmi2102@hotmail.com'
    # Set up the email object
    msg = EmailMessage()

    # Set up the email message
    msg.set_content(body)
    msg['subject'] = "Python tip of the day!\n"
    msg['to'] = to
    msg['from'] = user

    # Set up the SMTP server and send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()


if __name__ == '__main__':
    # Generate the Python tip and send it
    tip = tip_generator()
    send_text(tip)

