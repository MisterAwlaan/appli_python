import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_FROM = "nidri@guardiaschool.fr"
EMAIL_PASSWORD = "thdk thiu jxld soqj"  # Remplacez par votre mot de passe d'application

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, to_email, msg.as_string())
        server.quit()
    except smtplib.SMTPAuthenticationError as e:
        print(f"Erreur d'authentification SMTP : {e}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")




'''def test_send_email():
    to_email = "nahilou.idri@gmail.com"  # Remplacez par l'adresse e-mail de test
    subject = "Test d'envoi d'e-mail"
    body = "Ceci est un e-mail de test envoyé depuis le script de test."

    send_email(to_email, subject, body)

if __name__ == "__main__":
    test_send_email()'''