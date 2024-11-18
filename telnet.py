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
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    # Crear las partes del mensaje
    text_part = MIMEText(body, 'plain')

    # Leer el archivo HTML
    html_part = MIMEText(f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }}
                    .container {{
                        width: 100%;
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        text-align: center;
                    }}
                    h1 {{
                        color: #333333;
                    }}
                    h2 {{
                        color: #555555;
                    }}
                    p {{
                        color: #777777;
                    }}
                    .button {{
                        display: inline-block;
                        padding: 10px 20px;
                        font-size: 16px;
                        color: #ffffff;
                        background-color: #007bff;
                        border-radius: 5px;
                        text-decoration: none;
                        margin-top: 20px;
                    }}
                    .footer {{
                        text-align: center;
                        padding: 10px;
                        font-size: 12px;
                        color: #aaaaaa;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwFNZjh5-XOKRbSfhYmq2YxnMouqQw9v4n6A&s" alt="Bienal Logo" style="width:100%; max-width:200px; margin-bottom:20px;">
                    <h1>BIENVENIDO AL SITIO DE LA BIENAL</h1>
                    {body}
                </div>
                <div class="footer">
                    <p>&copy; 2024 Bienal. Todos los derechos reservados.</p>
                </div>
            </body>
        </html>
        """, 'html')

    # Adjuntar las partes al mensaje
    msg.attach(text_part)
    msg.attach(html_part)

    try:
        # Conectarse al servidor SMTP
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Iniciar TLS para seguridad
            server.login(sender_email, password)  # Iniciar sesión en el servidor SMTP
            server.sendmail(sender_email, to_email, msg.as_string())  # Enviar el correo electrónico
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")



'''
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
'''
