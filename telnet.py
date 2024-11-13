import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config

def send_email(subject, body, to_email):
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender_email = config('EMAIL_HOST_USER')
    password = config('EMAIL_HOST_PASSWORD')

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Agregar el cuerpo del mensaje
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Conectarse al servidor SMTP
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Iniciar TLS para seguridad
            server.login(sender_email, password)  # Iniciar sesión en el servidor SMTP
            text = msg.as_string()
            server.sendmail(sender_email, to_email, text)  # Enviar el correo electrónico
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")