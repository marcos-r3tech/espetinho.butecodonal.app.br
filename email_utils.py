import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

def enviar_email_backup(destinatario, remetente, senha, arquivo_backup):
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = 'Backup Automático - Buteco do Nal'
    
    corpo = 'Segue em anexo o backup automático do sistema Buteco do Nal.'
    msg.attach(MIMEText(corpo, 'plain'))

    # Anexar arquivo
    with open(arquivo_backup, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(arquivo_backup)}"')
        msg.attach(part)

    # Enviar e-mail
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())
        server.quit()
        print(f"✅ Backup enviado por e-mail para {destinatario}")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")
        return False
