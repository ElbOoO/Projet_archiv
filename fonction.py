import os
import smtplib
import ssl
from email.message import EmailMessage
import urllib.request
import json
import logging
import zipfile
import tarfile
import pysftp
import datetime


with open('./config.json', 'r') as file:
    data = json.load(file)


#sftp
def sftpUpload(fileName):
    try:
        with pysftp.Connection(data["sftp"]["hostname"], username=data["sftp"]["username"],
                               password=data["sftp"]["password"]) as sftp:
            sftp.put(fileName)  # upload file to public/ on remote
    except Exception as e:
        logging.error(e)


def sftpDownload(fileName):
    try:
        with pysftp.Connection(data["sftp"]["hostname"], username=data["sftp"]["username"],
                               password=data["sftp"]["password"]) as sftp:
            sftp.get(fileName)  # get a remote file
    except Exception as e:
        logging.error(e)

# gestion du fichier


logging.basicConfig("log.txt", level=logging.DEBUG,format='%(asctime)s -- %(levelname)s -- %(message)s')

class Traitement_fichier:
    def recupZip(url):
        to = "sav" + datetime.datetime.now().strftime(data["source"]["dateFormat"])
        try:
            urllib.request.urlretrieve(url, to + ".zip")
            logging.info("Telechargement du fichier %s effectuée avec succes ", data["source"]["zipName"])
            return to
        except Exception as e:
            logging.error(e)

    def Nettoyage(fileName):
        logging.info("Nettoyage de la dernière sauvegarde")
        files = {fileName + '.zip', fileName + '.tar.gz', 'dumb.db'}
        for i in files:
            if os.path.exists(i):
                os.remove(i)


    def Verification(zipName):
        logging.info("verifiation du zip :" + zipName)
        try:
            with zipfile.ZipFile(zipName) as zip:
                if zip.namelist()[0].split(".")[-1] != data["source"]["ext"]:
                    raise NameError("Mauvais type : le fichier zippé ne contient pas de fichier db")
                else:
                    date = (datetime.datetime(*zip.infolist()[0].date_time[0:6]))
                    logging.info("Le fichier .db a été trouvé")
                    logging.info("Date du fichier : " + str(date))
        except Exception as e:
            logging.error(e)


    def extractZip(zipName):
        logging.info("Extraction du fichier :" + zipName)
        try:
            with zipfile.ZipFile(zipName, 'r') as zfile:
                zfile.extractall()
        except Exception as e:
            logging.error(e)


    def makeTarfile(output_filename, source_dir):
        logging.info("Compression en tar.gz du fichier :" + output_filename)
        try:
            with tarfile.open(output_filename, "w:gz") as tar:
                tar.add(source_dir, arcname=os.path.basename(source_dir))
            logging.info("L'archive %s a bien été crée !", output_filename)
        except Exception as e:
            logging.error(e)



class Mail:

    def mail(objet, to, corps):
        msg = EmailMessage()
        msg.set_content(corps)
        msg["Subject"] = objet
        msg["From"] = data["mail"]["login"]
        msg["To"] = to

        context = ssl.create_default_context()
        with smtplib.SMTP(data["mail"]["hostname"],data["mail"]["port"]) as smtp:
            smtp.starttls(context=context)
            smtp.login(data["mail"]["login"], data["mail"]["password"])
            smtp.send_message(msg)