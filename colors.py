import os
directory=os.path.dirname(__file__)
COLORS={
        "RED" :(233, 53, 53),
        "OUR_BLACK" :(33, 33, 33),
        "BTN_GREY" :(196, 196, 196),
        "HOVER_GREY" :(114,114,114),
        "GRIS":(120, 124, 126),
        "VERT":(106, 170, 100),
        "JAUNE":(201, 180, 88),
        "WHITE" :(255,255,255),
        "BLACK":(0,0,0)
    }

import json

def getLangue():
    with open(directory+r"\settings.json") as f:
        settings=json.load(f)

    return settings["langue"]

def getMode():
    with open(directory+r"\settings.json") as f:
        settings=json.load(f)
    
    if settings["modeDark"] :
        return "dark"
    else:
        return "light"

def changeMode():
    
    with open(directory+r"\settings.json") as f:
        settings=json.load(f)
    
    settings["modeDark"]=not settings["modeDark"]
    
    with open(directory+r"\settings.json","w") as f:
        json.dump(settings,f)


def getLangue():
    with open(directory+r"\settings.json") as f:
        settings=json.load(f)
    
    return settings["langue"]

def changeLang() :
    with open(directory+r"\settings.json") as f:
        settings=json.load(f)

    if settings["langue"] == "en":
        settings["langue"]="fr"
    else :
        settings["langue"]="en"
    
    with open(directory+r"\settings.json","w") as f:
        json.dump(settings,f)

def getTXT():
    # print("getTXT")
    if getLangue()=="en":
        return {
        "main_play" : "PLAY" ,
        "main_stats" : "STATS" ,
        "main_about" : "ABOUT",
        "main_quit" : "QUIT" ,
        #--------continue----------#
        "cont_cont" : "CONTINUE",
        "cont_new" : "NEW GAME" ,
        "cont_word" : "WORD LENGTH",
        #----------stats------------#
        "stats_stats" : "STATS",
        "stats_longeur" : "LENGTH ",
        #----------QUIT------------#
        "quit_sure1" : "Are you sure you",  
        "quit_sure2" : "want to quit ?", 
        "quit_quit" : "Quit Motus",
        "quit_cancel" : "Cancel",    
        #----------about------------#
        "about_about" : "ABOUT ", 
        "about_txt1" : "Motus is a word search game.",
        "about_txt2" : "It is presented in the form of a grid, where each",
        "about_txt3" : " tile contains a letter of the searched word.",  
        "about_rul1" : "The letter belongs to the word and well placed",
        "about_rul2" : "The letter belongs to the word but misplaced",
        "about_rul3" : "The letter does not belong to the word",  
        "about_rul4" : "The word does not belong in the dictionary", 
        #--------language----------#
        "lang_lang" : "LANGUAGE :",
        "lang_en" : "ENGLISH" ,
        "lang_fr" : "FRENCH",
        }
    else :
        return {
        "main_play" : "JOUER",
        "main_stats" : "SCORE",
        "main_about" : "A PROPOS",
        "main_quit" : "QUITER",
        #--------continue----------#
        "cont_cont" : "CONTINUER",
        "cont_new" : "NOUV PARTIE" ,
        "cont_word" : "LANGUEUR DU MOT",
        #----------stats------------#
        "stats_stats" : "STATISTIQUE",
        "stats_longeur" : "LANGUEUR ",
        #----------QUIT------------#
        "quit_sure1" : "Voulez vous vraiment", 
        "quit_sure2" : "Quitter ?",
        "quit_quit" : "Quitter",
        "quit_cancel" : "Annuler",   
        #----------about------------#
        "about_about" : "A PROPOS", 
        "about_txt1" : "Motus est un jeu de recherche de mots.",
        "about_txt2" : " Il est présenté sous forme de grille, où chaque",
        "about_txt3" : " carreau contient une lettre du mot recherché.",  
        "about_rul1" : "   La lettre appartient au mot et bien placé",
        "about_rul2" : "   La lettre appartient au mot mais mal placé",
        "about_rul3" : "   La lettre n’appartient pas au mot",  
        "about_rul4" : "   Le mot n’appartient pas au dictionnaire",  
        #--------language----------#
        "lang_lang" : "LANGUE :",
        "lang_en" : "ANGLAIS" ,
        "lang_fr" : "FRANCAIS",
        }

# TXT=getTXT()