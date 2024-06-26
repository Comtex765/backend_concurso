import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body, to_email):
    from_email = "ferchon123443@gmail.com"
    app_password = "ijex txxz nwmj tefy"  # La contraseña de aplicación generada

    # Crear el contenedor del mensaje
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    # Agregar el cuerpo del mensaje
    msg.attach(MIMEText(body, "plain"))

    # Conectar al servidor de Gmail y enviar el correo
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Iniciar TLS para seguridad
        server.login(from_email, app_password)  # Iniciar sesión con la cuenta de Gmail
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()  # Cerrar la conexión al servidor
        print("Correo enviado con éxito")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
