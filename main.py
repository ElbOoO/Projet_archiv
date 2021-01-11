from fonction import *


url = "http://127.0.0.1:8888/"

if __name__ == '__main__':
    try:

        # On définit le nom de la sauvegarde
        fileName = "sav" + datetime.datetime.now().strftime(data["source"]["dateFormat"])

        # on definit le nom du zip de sauvegarde
        zipName = fileName + ".zip"

        # on definit le nom du tar.gz de sauvegarde
        tarName = fileName + ".tar.gz"

        # on nettoye les fichiers temporaires qui pourrait creer des conflits
        Traitement_fichier.Nettoyage(fileName)

        # on va chercher le zip sur le server web
        Traitement_fichier.recupZip(data["source"]["url"])

        # on verifie le contenu du zip
        Traitement_fichier.Verification(zipName)

        # on dézip le fichier
        Traitement_fichier.extractZip(zipName)

        # on le recompresse au format Tar.ge
        Traitement_fichier.makeTarfile(tarName, data["source"]["name"])

        # on l'envoie sur le serveur distant
        sftpUpload(tarName)

        # on envoie un mail en cas de réussite
        Mail.mail("réussite", data["mail"]["to"], "corps")

    except Exception as e:
        print(e)
        logging.critical(e)
        Mail.mail("echec", data["mail"]["to"], e)