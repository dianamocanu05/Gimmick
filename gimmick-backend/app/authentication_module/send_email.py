import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

GIMMICK_EMAIL_ADDRESS = "gimmick.app.tech@gmail.com"
GIMMICK_EMAIL_PASSWORD = "lipx nlwh itxw mkar"
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


def send_signup_confirmation_email_to_user(email):
    msg = MIMEMultipart()
    msg['From'] = GIMMICK_EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = 'GIMMICK - Sign up confirmation'

    with open('templates/signup_confirmation_template.html') as template:
        html_message = template.read()
    html_part = MIMEText(html_message, 'html')
    msg.attach(html_part)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(GIMMICK_EMAIL_ADDRESS, GIMMICK_EMAIL_PASSWORD)

    server.send_message(msg)

    server.quit()


if __name__ == "__main__":
    send_signup_confirmation_email_to_user('antonioioanghibu@gmail.com')
