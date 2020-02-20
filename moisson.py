# coding : utf-8

# Ici, je vais importer les modules nécessaires

import csv
import json
import requests

# Création du fichier

fichier = "jugementsassurance.csv"

# Création de la première requête envoyée à l'API de la CANLII. 

url = "https://api.canlii.org/v1/caseBrowse/fr/?api_key=tGkCa6Ljss2AH1ZZHlU9IaLz8QL42Q5s7WoZCQ4D"

entetes = {
    "User-Agent":"Charles Mathieu - 514-746-5481 : requête envoyée dans le cadre d'une démarche journalistique", 
    "From":"charlesbmathieu@hotmail.com"
}

r = requests.get(url,headers=entetes)

print(r)

# En fait, cette première requête permet d'obtenir les différents codes des tribunaux du Canada.


if r.status_code == 200:
    tribunaux = r.json()
    for tribunal in tribunaux["caseDatabases"]:
        if tribunal["jurisdiction"] == "qc":
            
            # J'ai décidé d'aller chercher les codes des différents tribunaux du Québec seulement, afin de limiter la quantité de jugements que je vais obtenir. 
            # Ici je vais créer une liste des codes afin de pouvoir l'utiliser plus tard lors d'une deuxième requête. 
            listeID = []
            # Définition de la variable IDtribunaux afin de pouvoir l'ajouter dans une liste. 
            IDtribunaux = tribunal["databaseId"]
            listeID.append(IDtribunaux)
            # print(listeID)
            for i in listeID:
                
                # Création d'une boucle permettant de formater le deuxième URL utilisé pour la prochaine requête. 

                url1 = "https://api.canlii.org/v1/caseBrowse/fr/{}/?offset=0&resultCount=10000&&decisionDateAfter=2018-12-31&api_key=tGkCa6Ljss2AH1ZZHlU9IaLz8QL42Q5s7WoZCQ4D"
                url2 = url1.format(i)
                
                # Ici, j'ai envoyé la deuxième requête, qui me permet d'aller chercher les différentes décisions, leur titre, une "citation" et le code de chaque décision qui a été déposé sur la CANLII. 

                r2 = requests.get(url2,headers=entetes)

                if r2.status_code == 200:
                    decisions = r2.json()
                    for decision in decisions["cases"]:
                         if "surance" in decision["title"]:
                            
                            # Cette condition me permet d'aller chercher les décisions qui contiennent uniquement le mot "surance" pour aller chercher les décisions ayant les mots "assurance" et "insurance" dans le titre. 
                            
                            listejugements = []
                            
                            # Création d'une liste et des variables qui seront mises dans la liste. 
                            
                            tribunal1 = decision["databaseId"]
                            titre = decision["title"]
                            citation = decision["citation"]
                            IDdossier = decision["caseId"]
                                
                            listejugements.append(titre)
                            listejugements.append(citation)
                            listejugements.append(tribunal1)
                            
                            # Parce que des fois, le code est dans IDdossier["fr"] ou dans IDdossier["en"], j'ai dû créer une condition afin que lorsque c'Est en "fr", il l'ajoute à une certaine liste, et que lorsque c'est en "en", il l'ajoute aussi. 

                            for e in IDdossier:
                                listeidcase = []
                                if "fr" in e:
                                    idf = IDdossier["fr"]
                                elif "en" in e:
                                    idf = IDdossier["en"]
                                listejugements.append(idf)
                                
                                # Pour être en mesure de cibler toutes les décisions, j'ai créé une nouvelle liste avec tous les codes des différents jugements. 
                                
                                listeidcase.append(idf)
                                
                                # Création d'une nouvelle boucle afin d'ajouter toutes les décisions dans le troisième URL utilisé pour la troisième requête. 

                                for c in listeidcase:

                                    # Je vais formater les différents URL, dans lesquels j'ai ajouté des accolades afin de pouvoir aller cibler tous les codes des jugements et tous les codes des tribunaux. 

                                    url3fin = "/{}/?api_key=tGkCa6Ljss2AH1ZZHlU9IaLz8QL42Q5s7WoZCQ4D".format(c)
                                    url3debut = "https://api.canlii.org/v1/caseBrowse/fr/{}".format(i)
                                    url3 = url3debut + url3fin
                                    
                                    r3 = requests.get(url3,headers=entetes)
                                    # La troisième requête me permet d'aller chercher la date de décision et les "keywords", qui indiquent ce dont il a été question dans la décision en question. Je crois que je vais tenter de filtrer tous les jugements en fonction des "keywords" la prochaine fois que je vais fouiller dans cet API. 
                                    if r3.status_code == 200:
                                        detailsJ = r3.json()
                                        # Création des variables et ajout de celles-ci à la liste des jugements utilisée pour créer le fichier CSV. 
                                        datedecision = detailsJ["decisionDate"]
                                        sujets = detailsJ["keywords"]
                                        listejugements.append(datedecision)
                                        listejugements.append(sujets)

                            # Création du fichier CSV. J'ai utilisé mon nom et celui de ma copine pour lui montrer que je l'aime. Vive la Saint-Valentin..!

                            Charles = open(fichier, "a")
                            Lea = csv.writer(Charles)
                            Lea.writerow(listejugements)
