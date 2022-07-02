def stats():
    import pygame
    from assets import Button 
    import os
    from quit import quitInterface,takeBluredScreenshot
    from fonctions import addToList
    from fonctions import removeFromList
    from fonctions import interfaceDecider
    import json

    directory = os.path.dirname(__file__)


    #------le dictionnaire utilisé pour le changemment de langue-------#
    from colors import getLangue
    from colors import changeLang
    from colors import getTXT

    TXT=getTXT() #le dictionnaire avec les mots affiche , utilise pour changement entre les langues
    #------------------------------------------------------------#



    #-----DARK/LIGHT----
    from colors import COLORS
    from colors import getMode
    
    MODE=getMode()
    if MODE=="dark":
        bgColor=COLORS["OUR_BLACK"]
        textColor=COLORS["WHITE"]
        btnTextColor=COLORS["OUR_BLACK"]
        btnColor=COLORS["BTN_GREY"]
        btnColorHover=COLORS["HOVER_GREY"]
    elif MODE=="light":
        bgColor=COLORS["WHITE"]
        textColor=COLORS["HOVER_GREY"]
        btnTextColor=COLORS["WHITE"]
        btnColor=COLORS["HOVER_GREY"]
        btnColorHover=COLORS["BTN_GREY"]
    #-------------------
    pygame.init()

    HIGHT=630
    WEIGHT=425

    DISPLAY=pygame.display.set_mode((WEIGHT,HIGHT))
    DISPLAY.fill(bgColor)
   
     #a partir du fichier score,sjon on recupere les top 5 scores et les longueurs des mots
    with open(directory+r"\score.json") as f :
         data_score = json.load(f)
         score1  = data_score["score1"]
         length1 = data_score["length1"]
         score2  = data_score["score2"]
         length2 = data_score["length2"]
         score3  = data_score["score3"]
         length3 = data_score["length3"]
         score4  = data_score["score4"]
         length4 = data_score["length4"]
         score5  = data_score["score5"]
         length5 = data_score["length5"]
    
     # on met le contenu du ficheir score.json (qui contient les top 5 scores et la longueur du mot) dans ces boutons

    carre = [Button(TXT["stats_stats"],(42,77),size=(345,106),bodyColor=bgColor,textColor=textColor),Button("TOP 5",(173,154),size=(83,42),bodyColor=bgColor,textColor=textColor)
            ,Button("SCORE",(104,223),size=(110,35),bodyColor=btnColor,textColor=btnTextColor),Button(TXT["stats_longeur"],(216,223),size=(110,35),bodyColor=btnColor,textColor=btnTextColor)
            ,Button(score1,(104,260),size=(110,35),bodyColor=btnColor,textColor=btnTextColor),Button(length1,(216,260),size=(110,35),bodyColor=btnColor,textColor=btnTextColor)
            ,Button(score2,(104,297),size=(110,35),bodyColor=btnColor,textColor=btnTextColor),Button(length2,(216,297),size=(110,35),bodyColor=btnColor,textColor=btnTextColor)
            ,Button(score3,(104,334),size=(110,35),bodyColor=btnColor,textColor=btnTextColor),Button(length3,(216,334),size=(110,35),bodyColor=btnColor,textColor=btnTextColor)
            ,Button(score4,(104,371),size=(110,35),bodyColor=btnColor,textColor=btnTextColor),Button(length4,(216,371),size=(110,35),bodyColor=btnColor,textColor=btnTextColor)
            ,Button(score5,(104,408),size=(110,35),bodyColor=btnColor,textColor=btnTextColor),Button(length5,(216,408),size=(110,35),bodyColor=btnColor,textColor=btnTextColor)]
    stats_back = Button(" ",imagepath=directory+"\\assets\\arrowForDark.svg",position=(16,16))




    run=True
    while run:
        stats_back.render(DISPLAY)
        for i in range(len(carre)):
            carre[i].render(DISPLAY)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                takeBluredScreenshot(DISPLAY)
                addToList(quitInterface)
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if stats_back.clicked():
                    removeFromList()
                    run=False

        pygame.display.flip()
    interfaceDecider()