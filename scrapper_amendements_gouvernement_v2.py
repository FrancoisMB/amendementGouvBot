#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 16:55:51 2020

@author: francoismalaussena
"""



from pathlib import Path
from datetime import datetime, timedelta
from lxml import html
import os, time, tweepy, requests, copy, re
from PIL import Image
from selenium import webdriver


# # set le dossier de travail à l'endroit où se trouve 
path_wd = r"C:\Users\Francois\Documents\Code_Python\scrapper_amendements_gouvernement"
os.chdir(path_wd)

PHANTOMJS_PATH = r"..\phantomjs-2.1.1-windows\bin\\"
driver = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH + 'phantomjs')    

# 2) initier des fichiers
if not os.path.exists('date_dernier_run.txt'):
    Path('date_dernier_run.txt').touch()
f = open("date_dernier_run.txt", "r")
date_dernier_run = f.read()
f.close()
print("date_dernier_run =", date_dernier_run)

# connexion à twitter
consumer_key = "xxx"
consumer_secret = "xxx"
access_token = "xxx"
access_secret = "xxx"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


send_to_twitter = True


#%%



    
    # # desired_capabilities = webdriver.DesiredCapabilities.PHANTOMJS.copy()
    # # desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) ' \
    # #                                                               'AppleWebKit/537.36 (KHTML, like Gecko) ' \
    # #                                                               'Chrome/39.0.2171.95 Safari/537.36'
    # # driver = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH + 'phantomjs', desired_capabilities=desired_capabilities)
    # driver.get('http://www.assemblee-nationale.fr/dyn/15/amendements/3397/AN/356')
    # e = driver.find_element_by_xpath('//*[@id="amendementCard"]/div[3]/div[4]')
    # start_height = e.location['y']
    # block_height = e.size['height']
    
    # start_width = e.location['x']
    # block_width = e.size['width']

    # driver.save_screenshot('./tmp.png')
    # img = Image.open('./tmp.png')
    
    # # draw = ImageDraw.Draw(img)
    # # draw.rectangle(((start_width, start_height), (start_width+block_width, start_height+block_height)), fill="red")
   
    # img2 = img.crop((start_width-5, start_height, start_width+block_width+5, start_height+block_height))
    # timestamp = str(int(time.time()))
    # filename = timestamp
    # img2.save('./output/' + filename + '.png')


while True:
    pass
    
    #%%
    # AN : 
    try:
        if not os.path.exists('liste_amendements_AN.txt'):
            Path('liste_amendements_AN.txt').touch()
        f = open("liste_amendements_AN.txt", "r")
        liste_amendements_last_time_AN = f.read()
        f.close()
        
        liste_amendements_last_time_AN = liste_amendements_last_time_AN.split("\n")
        liste_amendements_this_time_AN = []
        
        
        # on va là : 
        # http://www2.assemblee-nationale.fr/recherche/amendements?LEGISLATURE=15#listeResultats=true&idDossierLegislatif=&idExamen=&miss&missionVisee=&numAmend=&idAuteur=ID_GVT&premierSignataire=true&idArticle=&idAlinea=&sort=&sousReserveDeTraitement=&dateDebut=&dateFin=&periodeParlementaire=&texteRecherche=&zoneRecherche=tout&nbres=50&format=html&regleTri=date&ordreTri=decroissant&start=1
        # http://www2.assemblee-nationale.fr/recherche/amendements               #listeResultats=tr u&idDossierLegislatif=&idExamen=     &missionVisee=&numAmend=&idAuteur=ID_GVT&premierSignataire=true&idArticle=&idAlinea=&sort=&sousReserveDeTraitement=&dateDebut=&dateFin=&periodeParlementaire=&texteRecherche=&zoneRecherche=tout&nbres=10&format=html&regleTri=date&ordreTri=decroissant&start=1
        # jsp trop la diff entre les deux liens
        # mais il y a bien commission ET séance
        # 
        
        nb_amendements_a_retourner = 500
        url_AN = "http://www2.assemblee-nationale.fr/recherche/query_amendements?typeDocument=amendement&leg=15&idExamen=&idDossierLegislatif=&missionVisee=&numAmend=&idAuteur=ID_GVT&premierSignataire=true&idArticle=&idAlinea=&sort=&sousReserveDeTraitement=&dateDebut=&dateFin=&periodeParlementaire=&texteRecherche=&format=html&tri=datedesc&start=1&typeRes=liste&rows="+str(nb_amendements_a_retourner)
        page_AN = requests.get(url_AN)
        
        date_du_jour = page_AN.json()["data_table"][0].split("|")[9]
        
        for i in range(nb_amendements_a_retourner):
            ligne_tableau_amendements = page_AN.json()["data_table"][i].split("|")
            osef, num_texte, nom_texte, osef, organe_amendement, num_amendement, lien_amendement, place_amendement, osef, date_amendement, osef, osef, mission_amendement, osef = ligne_tableau_amendements
            
            if date_amendement != date_du_jour:
                #print("on est dans les amendements du",date_amendement,"et plus dans ceux du",date_du_jour, "donc on s'arrête")
                break
            
            del osef
            
            # num_texte = ligne_tableau_amendements[1]
            # nom_texte = ligne_tableau_amendements[2]
            # num_amendement = ligne_tableau_amendements[5]
            # lien_amendement = ligne_tableau_amendements[6]
            # organe_amendement = ligne_tableau_amendements[4]
            # place_amendement = ligne_tableau_amendements[7].lower()
            # mission_amendement = ligne_tableau_amendements[12].lower()
            
            place_amendement = place_amendement.lower()
            
            if mission_amendement != "":
                mission_amendement = " "+mission_amendement.lower()
           
            if organe_amendement == "Séance publique" or organe_amendement.startswith("Commission spéciale") or organe_amendement.startswith("Commisssion spéciale"):
                pass
            else:
                organe_amendement = "Commission des " + organe_amendement   
         
            str_a_tweeter_AN = """[AN]
Organe : {0}
Amendement : {1}
Place : {2}{3}
Texte : {4}""".format(organe_amendement,
                num_amendement,
                place_amendement,
                mission_amendement,
                nom_texte
                )
                
            tweet_size = 280 - 24 -7
            if len(str_a_tweeter_AN) > tweet_size:
                str_a_tweeter_AN = str_a_tweeter_AN[:tweet_size-4] +"..."
            str_a_tweeter_AN += """
Lien : """ + lien_amendement
            #print(str_a_tweeter_AN)  
        
            id_unique_amendement_AN = num_texte + "-" + num_amendement
            #print(id_unique_amendement_AN)
            liste_amendements_this_time_AN.append(id_unique_amendement_AN)
            
            
            if not id_unique_amendement_AN in liste_amendements_last_time_AN:
                
                ##### partie où on essaie de faire un screenshot de l'exposé des motifs ###
                print("1") 
                try:
                    driver.get(lien_amendement)
                    #driver.get('http://www.assemblee-nationale.fr/dyn/15/amendements/3604/AN/1')
                    time.sleep(0.1)
                    try:
                        e = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div')
                        if e.text == "Veuillez nous excuser, l'amendement visé n'est pas disponible. Il est possible cet amendement ne soit pas encore publié.":
                            continue
                    except:
                        pass
                    
                    try:
                        e = driver.find_element_by_xpath('//*[@id="amendementCard"]/div[3]/div[4]')
                    except Exception as err:
                        print("Impossible de récupérer le Xpath de l'exposé des motifs l'amendement :", lien_amendement)
                        print(err)
                        continue
                    time.sleep(0.1)
                    start_height = e.location['y']
                    time.sleep(0.1)
                    block_height = e.size['height']
                    time.sleep(0.1)
                    
                    start_width = e.location['x']
                    time.sleep(0.1)
                    block_width = e.size['width']
                    time.sleep(0.1)
                
                    img_path_1 = './img_output/'+id_unique_amendement_AN+'_1.png'
                    img_path_2 = './img_output/'+id_unique_amendement_AN+'_2.png'
                    
                    driver.save_screenshot(img_path_1)
                    time.sleep(0.1)
                    img = Image.open(img_path_1)
                    time.sleep(0.1)
                    img2 = img.crop((start_width-5, start_height, start_width+block_width+5, start_height+block_height))
                    time.sleep(0.1)
                    img2.save(img_path_2)
                    time.sleep(0.1)
                except Exception as err:
                    print("Screenshot amendement AN raté (amendement non enregistré en base) :")
                    print(err)
                    continue
                ### fin tentative de screenshot exposé des motifs ###
                
                
                print()
                print(str_a_tweeter_AN)
                if send_to_twitter == True:   
                    try:
                        api.update_with_media(img_path_2, status = str_a_tweeter_AN)                            
                    except Exception as err:
                        enregistrement_erreur= err
                        try:
                            if err.api_code == 187:
                                print("Tweet déjà posté. Print de la liste des amendements last_time")
                                print(liste_amendements_last_time_AN)
                                print("et print de la liste des amendements this time")
                                print(liste_amendements_this_time_AN)
                            else:
                                print("Erreur lors du tweet ! Erreur :")
                                print(err)
                        except:
                            print("Erreur lors du tweet ! Erreur :")
                            print(err)
                        continue
    
                try:
                    os.remove(img_path_1) 
                except:
                    pass
                try:
                    os.remove(img_path_2)
                except:
                    pass
            
        try:
            with open("liste_amendements_AN.txt","w") as f:
                f.write('\n'.join(liste_amendements_this_time_AN))
        except Exception as err:
            enregistrement_erreur = err
            print("problème dans l'enregistrement dans le fichier AN")
            print(err)
    except Exception as err:
        enregistrement_erreur = err
        print("Erreur dans la boucle AN :")
        print(err)
   # del liste_amendements_last_time_AN, liste_amendements_this_time_AN
 
    
    # On peut faire l'identification unique de chaque amendement grâce à NumTexte+Num (+ éventuellement l' "organe", c'est à dire comm ou séance publique)
    # Pour les derniers, on clique sur le lien
    # Puis on prend un screen de l'amendement
    # Et on enregistre le nom du texte (qui est en haut de l'amendement)
    # Puis tweet :
    # Amdt XYZ en séance/commmission XYZ au PJL blabla http://urlVersLAmendement.com + screenshot
    
    
    
    
    
    #%%
    
    # Sénat
    
    try:
        if not os.path.exists('liste_amendements_S.txt'):
            Path('liste_amendements_S.txt').touch()
        f = open("liste_amendements_S.txt", "r")
        data_amendements_last_time_S = f.read()
        f.close()
        
        data_amendements_last_time_S = data_amendements_last_time_S.split("\n") #split le doc ligne par ligne
    
        # transforme une ligne avec 2020-11-16 22:33:46.096535|2020-2021-101-1066 en {"date_ajout":2020-11-16 22:33:46.096535, "id_unique_amendement":"2020-2021-101-1066"}
        # et l'ajoute dans une liste de dict [{}, {}, {}, {}]
        liste_dict_amendements_last_time_S = []
        for el in data_amendements_last_time_S:
            try:
                liste_dict_amendements_last_time_S.append({"date_ajout":datetime.strptime(el.split("|")[0], '%Y-%m-%d %H:%M:%S.%f'), "id_unique_amendement":el.split("|")[1]})
            except Exception as err:
                enregistrement_erreur = err
                print(err)
                pass
    
        # on sort la liste des id_unique_amendements pour plus tard regarder si l'id_unique_amendement de l'amendement examiné est dedans ou non
        liste_amendements_last_time_S = [el["id_unique_amendement"] for el in liste_dict_amendements_last_time_S]
    
        # la version last_time ne servira plus (je crois), la version this_time on lui appendera tout nouvel amendement (avec comme datetime now())
        liste_dict_amendements_this_time_S = liste_dict_amendements_last_time_S
    
    
        
        # on récupère ici les nums des textes discutés prochainement en séance :
        url_S = "http://www.senat.fr/dossiers-legislatifs/textes-recents.html"
        page_S = requests.get(url_S)
        tree = html.fromstring(page_S.content)
        
        if tree.text_content().find("Application Indisponible") != -1:
            print("site sénat indispo")
            continue
        
        # on va chercher le bloc html qui est dans le premier encadré de la page textes-recents.html du sénat
        dates = tree.xpath('//*[@id="main"]/div[1]/div[2]/ul')[0]
        
        liste_des_li = []
        for element in range(len(dates)): # puis le bloc de code html qui correspond à chaque date différente
            try:               
                date = dates[element]
                liste_des_li.extend(date.getchildren()[0].getchildren()) #chaque li est un texte différent je crois
            except:
                pass 
        
        # on met ça dans un dict {1 : { nom : projet de loi machin, lien:http://www.senat.fr/dossier-legislatif/pjl19-314.html } }
        dict_noms_et_liens_textes = {}
        dict_interm = {}
        i = 0
        for element in liste_des_li:
            dict_interm[i] = {"nom": element.getchildren()[0].text, "lien" : "http://www.senat.fr"+element.getchildren()[0].attrib["href"]}
            i += 1
        
        # on vire les duplicates du dict (parce qu'il est possible d'avoir 12 novembre PLFSS et 13 novembre PLFSS, et donc des doublons)
        for key, value in dict_interm.items():
            if value not in dict_noms_et_liens_textes.values():
                dict_noms_et_liens_textes[key] = value
        del dict_interm
        
        # faut récupérer pour chacun les trois derniers chiffres avant .html    # il y a des pieges genre plfss2021.html
         # on va appeler cette liste liste_numeros_textes (cf plus bas)
        # ce numéro est le numéro de la toute première version déposée devant le Sénat : le texte du gouv si le Sénat est première chambre, le texte de l'AN si le Sénat est 2ème chambre
        
        # mais dans le lien qu'on va construire plus loin, le numéro de texte utilisé quand ils s'agit des amendements de 2nde / nvelle lecture est le numéro
        # de la dernière version du texte, et plus le numéro de la première version déposée devant le Sénat
        #
        # IDEM POUR LES AMENDEMENTS DE SEANCE, MEME EN PREMIERE LECTURE
        
        # donc pour avoir les amendements de ces versions du texte, il faut ensuite aller sur la page du dossier législatif du texte
        # puis récupérer le nouveau numéro dans le lien sous le mot "Amendements".
        # Par exemple sur ce PJL : https://www.senat.fr/dossier-legislatif/pjl10-304.html
        # https://www.senat.fr/amendements/2010-2011/389/accueil.html <= ici on récupèrerait 389 pour les amendements de séance 1L
        # https://www.senat.fr/amendements/commissions/2010-2011/567/accueil.html <= 567 pour les amendements de commission 2L
        # https://www.senat.fr/amendements/2010-2011/572/accueil.html <= ici on récupèrerait 572 pour les amendements de séance 1L
        
        # En outre, on peut utiliser un truc du genre :
        # if dans la page il y a "nouvelle lecture" : 
        # elif dans la page il y a "deuxième lecture : 
        # else :
        # mais qui règle pas le problème pour les commissions. 
        # Autre solution sans doute meilleure : récupérer la dernière instance d'un lien qui contient "amendements"
        
        dict_noms_liens_texte_et_liens_amendements = {}
        for key, value in dict_noms_et_liens_textes.items():  # pour chacun des textes à l'ODJ
            # print(key, value["nom"], value["lien"])
            
            nom_texte = value["nom"]
            lien_texte = value["lien"]
            
            page_dossier_legislatif = requests.get(value["lien"])
            tree = html.fromstring(page_dossier_legislatif.content)
            div_dossier_legislatif = tree.xpath('//*[@id="box-timeline"]/div[2]')[0]
            
            # on va chercher le contenu des deux derniers div de la forme
            # <div class="item item-small" id="timeline-XX"> où XX = nombre à changer pour avoir les deux derniers
            # c'est à dire les deux dernières étapes en date de la procédure législative
            liste_div_deux_dernieres_etapes = div_dossier_legislatif.xpath("div[contains(@id,'timeline-')][position()>last()-2]")
        
        
            for div_etape_procedure in liste_div_deux_dernieres_etapes:
                # print(div_etape_procedure.text_content())
        
                liste_des_liens = div_etape_procedure.xpath('*//a/@href')
                liste_liens_amendements = [a for a in liste_des_liens if a.find("amendements") != -1] # liste des liens vers les pages d'amendements
                
                liste_liens_amendements = list(set(liste_liens_amendements)) # vire éventuels doublons, même si je crois que normalement il n'y en a pas
                
                if len(liste_liens_amendements) > 1:
                    print("il y a plus d'un lien amendements, c'est chelou :")
                    print(liste_liens_amendements)
                    continue
                
                if liste_liens_amendements:
                    #print(value["nom"])
                    #print(liste_liens_amendements)
        
                    texte_du_div = str(div_etape_procedure.text_content())
                    if texte_du_div.find("Séance publique") != -1:
                        # on est en séance publique
                        organe_amendement = "Séance publique"
                    elif texte_du_div.find("Travaux de commission") != -1:
                        # on est en commission
                        # et pour savoir laquelle, on va lire ce qui est écrit dans le premier amendement déposé
                        # pas sûr que ça soit exact si en fait tous les amendements de toutes les commissions sont mélangés
                        # mais bon, mieux que rien
                        # solution si jamais ce problème apparaît un jour : plutôt que de chercher la commission ici
                        # chercher la commisison plus tard, quand on a le lien de l'amendement du gouv,
                        # et allier lire directement dans l'amendement du gouv
                        
                        url_amendement_numero_1 = "http://www.senat.fr" + liste_liens_amendements[0][:-13] + "/Amdt_COM-1.html"
                        page_amendement_numero_1 = requests.get(url_amendement_numero_1)
                        tree_amendement_numero_1 = html.fromstring(page_amendement_numero_1.content)
                        table_dans_le_html = tree_amendement_numero_1.xpath('/html/body/div/table[1]')[0]
                        organe_amendement = str(table_dans_le_html.getchildren()[0].getchildren()[0].getchildren()[1].text_content())
                        
                        del url_amendement_numero_1, page_amendement_numero_1, tree_amendement_numero_1, table_dans_le_html
                                
                    else:
                        # on est ni en SP ni en comm parce que ce sont probablement les encarts en face des icones bleues et rouges de l'AN / du Sénat
                        # print(texte_du_div)
                        continue
        
        
        
                    # pour l'instant on a que le lien vers la page "rechercher des amendements", maintenant on va construire le lien vers la page 
                    # http://ameli.senat.fr/recherche/recherche.jsp?session=2019-2020&texte=
                    # + num_texte
                    # + &type_texte=C pour les amendements de commission, &type_texte=S pour les amendements de séance
                    # + &gouvernement=on&article=ALL&contenu=&sort=ALL&ordre=depot#resultats
                     
                    # et enfin, récupérer les résultats, mais ensuite, les parcourir dans le sens INVERSE : les derniers amendements sont tout en bas
                 
                    if liste_liens_amendements[0].find("commissions") != -1:
                        str_session, str_texte = liste_liens_amendements[0][25:-13].split("/")
                        type_texte = "C"
                        num_texte = str_session + "-" + str_texte
                    else:
                        str_session, str_texte = liste_liens_amendements[0][13:-13].split("/")
                        type_texte = "S"
                        num_texte = str_session + "-" + str_texte
                    lien_amendements = "http://ameli.senat.fr/recherche/recherche.jsp?session={0}&texte={1}&type_texte={2}&gouvernement=on&article=ALL&contenu=&sort=ALL&ordre=depot#resultats".format(str_session, str_texte, type_texte)
                    
                    # maintenant on va consulter le tableau des amendements
                    
                    page_amendements = requests.get(lien_amendements)
                    tree = html.fromstring(page_amendements.content)
                    try:
                        tableau_amendements = tree.xpath('/html/body/div[1]/div/div[1]/div[2]/div[3]/div[1]/div[2]/div/div[2]/div/table')[0]
                    except:
                        # ya pas de tableau parce qu'il n'y a pas d'amendement
                        continue
                    for element_du_tableau in tableau_amendements.getchildren()[2:]:
                        try:
                            num_amendement, place_amendement = element_du_tableau.getchildren()[0:2]
        
                            num_amendement = num_amendement.getchildren()[0]
                            lien_amendement = "http://"+num_amendement.attrib["href"][2:]
                            num_amendement = " ".join(re.split("\s+", num_amendement.text_content(), flags=re.UNICODE)).strip()
                            num_amendement = num_amendement[7:]
                            place_amendement = " ".join(re.split("\s+", place_amendement.text_content(), flags=re.UNICODE)).strip()
                            place_amendement = place_amendement.lower()
                            if place_amendement.find("rt. add.")!=-1:
                                place_amendement = "après l'"+place_amendement[16:]
                            #print(num_amendement, place)
                            
                            mission_amendement = "" # je peux pas l'avoir sans aller lire l'amendement sur sa page, flemme
                            
                            dict_noms_liens_texte_et_liens_amendements[key] = {
                                "nom_texte" : nom_texte,
                                "lien_texte" : lien_texte,
                                "lien_recherche_amendements" : liste_liens_amendements[0],
                                "lien_liste_amendements": lien_amendements,
                                "organe" : organe_amendement,
                                "place_amendement": place_amendement,
                                "num_amendement": num_amendement,
                                "lien_amendement": lien_amendement
                                }
                            
                            # print(dict_noms_liens_texte_et_liens_amendements)
                            
                        except Exception as e:
                            enregistrement_erreur = e
                            print(e)
                            print(nom_texte)
                            print(liste_liens_amendements[0])
                            print(lien_amendements)
                            print(element_du_tableau)
                            print(element_du_tableau.text_content())
                            print(" ")
                            continue
        
                        str_a_tweeter_S = """[Sénat]
Organe : {0}
Amendement : {1}
Place : {2}{3}
Texte : {4}""".format(organe_amendement,
                            num_amendement,
                            place_amendement,
                            mission_amendement,
                            nom_texte
                            )
                        #print(str_a_tweeter_S)
                        
                        tweet_size = 280 - 24 -7
                        if len(str_a_tweeter_S) > tweet_size:
                            str_a_tweeter_S = str_a_tweeter_S[:tweet_size-4] +"..."
                        str_a_tweeter_S += """
Lien : """ + lien_amendement
                        #print(str_a_tweeter_S)  
        
        
                        id_unique_amendement_S = num_texte + "-" + num_amendement
                        #print(id_unique_amendement_S)
                        if id_unique_amendement_S not in liste_amendements_last_time_S:
                            liste_dict_amendements_this_time_S.append({"date_ajout" : datetime.now(), "id_unique_amendement" : id_unique_amendement_S})
                            print(str_a_tweeter_S)
                            print()
                            if send_to_twitter == True:   
                                try:
                                                                    
                                    driver.get(lien_amendement)
                                    #driver.get('http://www.senat.fr/amendements/2020-2021/101/Amdt_1072.html')
                                    time.sleep(0.1)
                                    e = driver.find_element_by_xpath('//*[@id="contenu"]/p')
                                    time.sleep(0.1)
                                    start_height = e.location['y']
                                    time.sleep(0.1)
    
                                    e = driver.find_element_by_xpath('//*[@id="contenu"]/div[2]')
                                    time.sleep(0.1)
                                    start_width = e.location['x']
                                    time.sleep(0.1)
                                    block_width = e.size['width']
                                    time.sleep(0.1)
    
                                    block_height = (e.location['y'] - start_height) + e.size['height']
                                    time.sleep(0.1)
                                    
                                    img_path_1 = './img_output/'+id_unique_amendement_S+'_1.png'
                                    img_path_2 = './img_output/'+id_unique_amendement_S+'_2.png'
                                    
                                    driver.save_screenshot(img_path_1)
                                    time.sleep(0.1)
                                    img = Image.open(img_path_1)
                                    time.sleep(0.1)
                                    img2 = img.crop((start_width-5, start_height-5, start_width+block_width+5, start_height+block_height+5))
                                    time.sleep(0.1)
                                    img2.save(img_path_2)
                                    time.sleep(0.1)
                                    api.update_with_media(img_path_2, status = str_a_tweeter_S)
                                    
                                    
                                except Exception as err:
                                    enregistrement_erreur = err
                                    if err.api_code == 187:
                                        print("Tweet déjà posté. Print de la liste des amendements last_time")
                                        print(liste_amendements_last_time_AN)
                                        print("et print de la liste des amendements this time")
                                        print(liste_amendements_this_time_AN)
                                    else:
                                        print("Erreur lors du tweet ! Erreur :")
                                        print(err)
                                os.remove(img_path_1) 
                                os.remove(img_path_2)
        
        try:
            with open("liste_amendements_S.txt","w") as f:
                f.write(
                    # on écrit en base toutes les lignes du dict qui ont moins d'un an
                    '\n'.join([str(el["date_ajout"])+"|"+el["id_unique_amendement"] for el in liste_dict_amendements_this_time_S if el["date_ajout"] > datetime.now()-timedelta(days=365)])
                    )
        except Exception as err:
            enregistrement_erreur = err
            print("problème dans l'enregistrement dans le fichier AN")
            print(err)          
    except Exception as err:
        enregistrement_erreur = err
        print("Erreur dans la boucle Sénat :")
        print(err)

   # del liste_amendements_last_time_S, liste_amendements_this_time_S

    #%%
    print(".", end="")
    time.sleep(120)
       
