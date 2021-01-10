import http.server
import urllib.request
import json
import logging
import pysftp


with open('./config.json', 'r') as file:
    data = json.load(file)

def lancer_serv(PORT = 8888, IP=""):
    PORT = 8888
    server_address = ("", PORT)

    server = http.server.HTTPServer
    handler = http.server.CGIHTTPRequestHandler
    handler.cgi_directories = ["/"]
    print("Serveur actif sur le port :", PORT)

    httpd = server(server_address, handler)
    httpd.serve_forever()

    print("mdrr")

def getZip(url):
 urllib.request.urlretrieve(url,"fic_arch.zip")

 print("ntm")

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


logging.basicConfig(filename=data["log"]["filename"], level=logging.DEBUG,
                    format='%(asctime)s -- %(levelname)s -- %(message)s')


def clean(fileName):
    logging.info("Nettoyage de la dernière sauvegarde")
    files = {fileName + '.zip', fileName + '.tar.gz', 'dumb.db'}
    for i in files:
        if os.path.exists(i):
            os.remove(i)


def checkZip(zipName):
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