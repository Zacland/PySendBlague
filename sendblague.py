# !/usr/bin/python
# -*- coding:Utf-8 -*-

import os
import configparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import urllib.request
import urllib.error


def create_config():
    config['SMTP'] = {
        'Host': 'smtp.gmail.com',
        'Email': 'toto@toto.com',
        'Password': '123456'
    }
    config['Sender'] = {
        'From': 'titi@tutu.com'
    }
    config['Receiver'] = {
        'To': 'lolo@gege.com'
    }
    with open('config.ini', 'w') as config_file:
        config.write(config_file)


def read_config():
    config.read('config.ini')


# -----
# MAIN
# -----
if __name__ == "__main__":

    config = configparser.ConfigParser()

    if not os.path.exists('./config.ini'):
        create_config()
    else:
        read_config()

    page = urllib.request.urlopen('http://blague.dumatin.fr/')
    str_page = page.read()

    soup = BeautifulSoup(str_page, 'html.parser')

    for div in soup.find_all("img"):
        div.decompose()

    titre = soup.find("div", {"id": "blaguedujour"}).find("h2")
    blague = soup.find("div", {"id" : "blaguedujour"}).findAll("p")

    sortie = titre.get_text() + '\n'
    for ligne in blague:
        sortie += ligne.get_text() + '\n'

    print(sortie)

    msg = MIMEMultipart()
    msg['From'] = config['SMTP']['Email']
    msg['To'] = config['Receiver']['To']
    msg['Subject'] = '[PiBlague] Blague du jour'
    msg['Content-Type'] = "text/html; charset=cp850"
    message = sortie
    msg.attach(MIMEText(message))

    print(msg)

    try:
        mail_server = smtplib.SMTP(config['SMTP']['Host'], 587)
        mail_server.ehlo()
        mail_server.starttls()

        mail_server.ehlo()
        mail_server.login(config['SMTP']['Email'], config['SMTP']['Password'])
        mail_server.sendmail(config['Sender']['From'], config['Receiver']['To'], msg.as_string())
        mail_server.quit()
        print("Mail envoyé !")
    except smtplib.SMTPAuthenticationError:
        print('Problème d\'authentification ! Vérifier User/Password.')
        quit()
    except smtplib.SMTPException as e:
        print(str(e.errno) + ' - ' + e.strerror)
        print("Err SMTP")
        quit()
    except:
        print("Problème !!")
        quit()

    print('Fini !')
