def game():
    import pygame
    import random
    import os
    import json
    

    from session_functions import DelAttempts
    from session_functions import SaveSession
    
    from word_definition_card import definitionInterface  #for rendering word definition
    from quit import quitInterface,takeBluredScreenshot
    
    from assets import Button
    from assets import checkword

    #---------------------------------------------------------------------------------------------
    from fonctions import removeFromList
    from fonctions import interfaceDecider
    from fonctions import addToList
    #---------------------------------------------------------------------------------------------
    from colors import COLORS



    pygame.init()
    # l'ICON du jeu
    # ICON = pygame.image.load("work_motus/assets/ICON.png")
    # pygame.display.set_caption("JEU MOTUS !")
    # pygame.display.set_icon(ICON)

    directory=os.path.dirname(__file__)
    sessionpath = directory+"\game_session.json"
    
    #Dimensions
    HEIGHT=630
    WIDTH=425
    TOP_MARGIN=70
    LR_MARGIN=58
    BETWEEN=5 #l'espace entre les carres
    


    #SCREEN
    SCREEN=pygame.display.set_mode([WIDTH,HEIGHT])
        
    RED =COLORS["RED"]
    OUR_BLACK =COLORS["RED"]
    BTN_GREY =COLORS["BTN_GREY"]
    HOVER_GREY =COLORS["HOVER_GREY"]
    GRIS=COLORS["GRIS"]
    VERT=COLORS["VERT"]
    JAUNE=COLORS["JAUNE"]
    WHITE =COLORS["WHITE"]

     #-----DARK/LIGHT----
    from colors import COLORS
    from colors import getMode
    
    MODE=getMode()
    if MODE=="dark":
        bg_color=COLORS["OUR_BLACK"]
        carre_color=COLORS["BTN_GREY"] 
        lettre_color=COLORS["OUR_BLACK"]
        color_interne=COLORS["OUR_BLACK"]

        textColor=COLORS["BTN_GREY"]
    elif MODE=="light":
        bg_color=COLORS["WHITE"]
        carre_color=COLORS["BTN_GREY"]
        lettre_color=COLORS["GRIS"]
        color_interne=COLORS["WHITE"]
        
        textColor=COLORS["HOVER_GREY"]
    #-------------------


    #le boutton de retour en arriére
    game_back = Button(" ",imagepath=directory+"\\assets\\arrowForDark.svg",position=(10,10))

    #button de definition de mot
    definitionBtn=Button("?",(WIDTH-93,HEIGHT-152),size=(20,25),textSize=90)

    #importation des données consérvé dans le fichier JSON
    with open(sessionpath,'r') as f:
        data = json.load(f)
        score = int(data["score"])

    #decision sur la longueur des mots 
    word_length= 6 if data["lengthsix"] else 5
    if(word_length==6): 
        LR_MARGIN=35
        TOP_MARGIN=80
    
    
    #déclaration de la taille du carrés utilisé
    carre_size=(WIDTH-2*LR_MARGIN-(word_length-1)*BETWEEN) // word_length
    
    FONT=pygame.font.Font(directory+"\\assets\\font\istok web\IstokWeb-Bold.ttf", int((70/100)*carre_size))
    FONT_END=pygame.font.Font(directory+"\\assets\\font\istok web\IstokWeb-Bold.ttf", 25)
    FONTSCORE = pygame.font.Font(directory+"\\assets\\font\istok web\IstokWeb-Bold.ttf", 20)
    
    #Chois du Dictionnare à importer
    from colors import getLangue
    if(data["lengthsix"]):
        if getLangue()=="en":
            from EN_wordsList import WORDS6 as WORDS
        else:
            from FR_wordsList import MOTS6 as WORDS #still not here
    else:
        if getLangue()=="en":
            from EN_wordsList import WORDS5 as WORDS
        else:
            from FR_wordsList import MOTS5 as WORDS

        

    #GAME
    M_INPUT=""
    INPUTS=[]
    if(data["guess"] == ""):            #s'il y a pas du mot à deviner dans la session
        ANSWER=random.choice(WORDS)
        f2 = open(sessionpath,'w')
        data["guess"] = ANSWER          #on ajout un nouveau mot à deviner
        json.dump(data,f2)
        f2.close()
    else:
        ANSWER = data["guess"]      #sinon on importe le mot qui existe déja

    #importer les tentatives s'ils existent
    for i in range(0,6):
        if(data["attempt"+str(i)] != ""):
            INPUTS.append(data["attempt"+str(i)])

    
    ScoreInc = False    #cette variable aide pour incrémenter le score une fois dans la boucle WHILE
    
    toBeRed=False #cette variable decide si le mot est incorrecte et va se coloré en ROUGE
 
    besoinNvClavier=True #pour Dessiner le clavier dans le cas ou on a besoin (le clavier n'existe pas a la fin du jeu)
    update_top5 = True #variable qui gére le score (TOP 5)

    FIN=False #pour decider si le jeu est fini
    run=True 
  
    while run:
        
        
        SCREEN.fill(bg_color)
        
        game_back.render(SCREEN) #pour afficher le bouton RETOUR EN ARRIERE
        
        if not FIN : #pour afficher le clavier dans le cas où le jeu n'est pas fini
            if besoinNvClavier:
                from clavier import Clavier
                clavier=Clavier(word_length,FONT_END,MODE)
                besoinNvClavier=False
            
            clavier.renderClavier(SCREEN)

        y=TOP_MARGIN
        for i in range(6) :
            x=LR_MARGIN
            for j in range(word_length) :
                
                carre=pygame.Rect(x,y,carre_size,carre_size)
                
                if MODE=="light" :
                    pygame.draw.rect(SCREEN,carre_color,carre,width=2)
                else :
                    pygame.draw.rect(SCREEN,carre_color,carre)

                if i<len(INPUTS) :#affichage du mot validé avec les colorations des caractéres
                    
                    color=checkword(ANSWER,INPUTS[i],V=VERT,Y=JAUNE,G=HOVER_GREY)
                    
                    pygame.draw.rect(SCREEN,color[j],carre)
                    
                    lettre=FONT.render(INPUTS[i][j],True,color_interne)
                    surface=lettre.get_rect(center=(x+carre_size//2,y+carre_size//2))
                    SCREEN.blit(lettre,surface)
                    
                    #coloration de clavier depandant de resultat de checkword
                    clavier.coloration(INPUTS[i][j],VERT,JAUNE,color[j])  

                    
                    
                if i==len(INPUTS) and  j<len(M_INPUT) : #affichage de chaque lettre entrer par le joueur 
                    lettre=FONT.render(M_INPUT[j],True,lettre_color)
                    surface=lettre.get_rect(center=(x+carre_size//2,y+carre_size//2))
                    SCREEN.blit(lettre,surface)

                x+=carre_size+BETWEEN  #passage au carré suivant
            y+=carre_size+BETWEEN #passage a la ligne (tentative) suivante

        #coloration du mot incorrecte en ROUGE
        if(len(M_INPUT)!= word_length):
            toBeRed=False
        if toBeRed :
            y=TOP_MARGIN
            yprime=y+(carre_size+BETWEEN)*(len(INPUTS))
            xprime=LR_MARGIN
            for k in range(len(M_INPUT)):
                color=RED
                carre=pygame.Rect(xprime,yprime,carre_size,carre_size)
                pygame.draw.rect(SCREEN,color,carre)
                
                lettre=FONT.render(M_INPUT[k],True,color_interne)
                surface=lettre.get_rect(center=(xprime+carre_size//2,yprime+carre_size//2))
                SCREEN.blit(lettre,surface)
                xprime+=carre_size+BETWEEN
        
              
        #affichage du Titre du Jeu          
        TITLE=FONT.render("MOTUS",True,textColor)
        surfaceTitle=TITLE.get_rect(center=(WIDTH/2,30))
        SCREEN.blit(TITLE,surfaceTitle)  

        #Affichage du Score Actuel
        SCORE_TEXT = FONTSCORE.render("Score: "+str(score), True,textColor)
        surfaceText = SCORE_TEXT.get_rect(topleft=(315, 12))
        SCREEN.blit(SCORE_TEXT,surfaceText)
        
        #Affichage de la ligne séparant le titre au contenu de page
        line=pygame.Rect(0,55,WIDTH,1)
        pygame.draw.rect(SCREEN,HOVER_GREY,line,width=5)

        
        
        if len(INPUTS) == 6 and INPUTS[5] != ANSWER.upper() :#si le joueur n'arrive pas a trouvé le mot dans 6 tentatives
            
            if update_top5 : #
                
                with open(directory+"\game_session.json","r") as f:
                    data = json.load(f)
                    scoreStats = data["score"]   #on sauvegarde le score pour les statistique
                    lengthStats = data["lengthsix"]
                

                with open(directory+"\score.json") as file :
                    sc_len = json.load(file)
                    top_5 = [(sc_len["score1"],sc_len["length1"]),(sc_len["score2"],sc_len["length2"]), (sc_len["score3"],sc_len["length3"]), (sc_len["score4"],sc_len["length4"]), (sc_len["score5"],sc_len["length5"])]
                    if(lengthStats):
                        word_length = 6
                    else:
                        word_length = 5 

                top_5.append((scoreStats,word_length))
                top_5.sort(key = lambda x: x[0], reverse =True)
            

                with open(directory+"\score.json") as fl:
                    scores_length = json.load(fl)   
                
                with open(directory+"\score.json","w") as fl:
                        scores_length["score1"]  = top_5[0][0]
                        scores_length["length1"] = top_5[0][1]
                        scores_length["score2"]  = top_5[1][0]
                        scores_length["length2"] = top_5[1][1]
                        scores_length["score3"]  = top_5[2][0]
                        scores_length["length3"] = top_5[2][1]
                        scores_length["score4"]  = top_5[3][0]
                        scores_length["length4"] = top_5[3][1]
                        scores_length["score5"]  = top_5[4][0]
                        scores_length["length5"] = top_5[4][1]
                        json.dump(scores_length,fl)
                        fl.close()
                update_top5 = False

            #on déclare la fin du jeu
            FIN = True

            #on supprime tout les tentatives du fichier JSON
            DelAttempts(sessionpath,data)
            
            #on remis le score à 0
            score = 0
            
            #affichage le mot rechercher
            lostMsg=FONT_END.render("The Word is \""+ANSWER.upper()+"\"",True,COLORS["RED"])
            surfaceLost=lostMsg.get_rect(center=(WIDTH/2-20,HEIGHT-140))
            SCREEN.blit(lostMsg,surfaceLost)

            #Affichage d'msg pour rejouer
            spaceMsg=FONT_END.render("Press SPACE to Play Again!",True,textColor)
            surfaceSpace=spaceMsg.get_rect(center=(WIDTH/2,HEIGHT-100))
            SCREEN.blit(spaceMsg,surfaceSpace)
            
            #Affichage du Score
            SCORE_TEXT = FONTSCORE.render("Score: "+str(score), True,textColor)
            surfaceText = SCORE_TEXT.get_rect(topleft=(315, 12))
            SCREEN.blit(SCORE_TEXT,surfaceText)

            #Affichage du Bouton de Definition
            definitionBtn.render(SCREEN)
            
            
            
            

        elif FIN == True : #si le jouer a trouver le mot rechercher

            #on supprime tout les tentatives du fichier JSON
            DelAttempts(sessionpath,data)
            
            #Affichage d'un msg de la gagne 
            winMsg=FONT_END.render("YOU WIN THE GAME!",True,COLORS["VERT"])
            surfaceWin=winMsg.get_rect(center=(WIDTH/2-20,HEIGHT-140))
            SCREEN.blit(winMsg,surfaceWin)

            #Affichage d'un msg pour rejouer
            spaceMsg=FONT_END.render("Press SPACE To Play Again!",True,textColor)
            surfaceSpace=spaceMsg.get_rect(center=(WIDTH/2,HEIGHT-100))
            SCREEN.blit(spaceMsg,surfaceSpace)
            
            #Affichage du Score
            SCORE_TEXT = FONTSCORE.render("Score: "+str(score), True,textColor)
            surfaceText = SCORE_TEXT.get_rect(topleft=(315, 12))
            SCREEN.blit(SCORE_TEXT,surfaceText)

            
            #incrémentation du score du joueur
            if(ScoreInc == False):
                score += 15 + 5*(6-len(INPUTS))
                ScoreInc = True
            
            #Affichage du Bouton de Definition
            definitionBtn.render(SCREEN) #Definition button
            
                
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT : #Si le joueur a quitter le jeu

                if FIN==False: #dans le cas où le jeu pas encore fini on sauvegarde les tentative du joueur
                    SaveSession(sessionpath,data,ANSWER,score,INPUTS,word_length)
                else: #si le jeu est fini en supprime toutes les tentatives
                    INPUTS=[]
                    ANSWER = random.choice(WORDS)
                    data["guess"] = ANSWER
                    SaveSession(sessionpath,data,ANSWER,score,INPUTS,word_length)
                
                #---------------------------------------------------------------------------------------------------
                #Affichage de l'interface QUIT
                takeBluredScreenshot(SCREEN)
                addToList(quitInterface)
                #---------------------------------------------------------------------------------------------------

                run=False #on pause la boucle WHILE

            if event.type==pygame.MOUSEBUTTONDOWN:
                
                #si le Bouton de définition est cliquer
                if definitionBtn.clicked():
                    takeBluredScreenshot(SCREEN)
                    addToList(definitionInterface)
                    run=False

                #si le boutton RETOUR EN ARRIERE est cliquer
                if game_back.clicked():
                    if FIN==False: #dans le cas où le jeu pas encore fini on sauvegarde les tentative du joueur
                        SaveSession(sessionpath,data,ANSWER,score,INPUTS,word_length)
                    else: #si le jeu est fini en supprime toutes les tentatives et on génére un nouveau mot à deviner
                        INPUTS=[]
                        ANSWER = random.choice(WORDS)
                        data["guess"] = ANSWER
                        SaveSession(sessionpath,data,ANSWER,score,INPUTS,word_length)
                    
                    removeFromList()
                    run=False
                

                toSave=False     #pour decider est ce que on a besoin de sauvegarder la session ou non
                
                #gerer les cliques des les btn de clavier
                [M_INPUT,INPUTS,FIN,toSave,ANSWER]=clavier.clickHandler(INPUTS,M_INPUT,FIN,ANSWER)

                #Sauvegarde les tentatives s'il est necessaire
                if toSave: SaveSession(sessionpath,data,ANSWER,score,INPUTS,word_length)

                
            if event.type == pygame.KEYDOWN :
               
               #Si on clique sur BACKSPACE
                if event.key == pygame.K_BACKSPACE  :
                    if len(M_INPUT)>0 :
                        M_INPUT=M_INPUT[:len(M_INPUT)-1] #on supprime le dérnier caractére du mot s'il est pas vide
                
               #Si on clique sur ESPACE
                if event.key == pygame.K_SPACE and FIN ==True:
                    update_top5 = True
                    M_INPUT=""
                    INPUTS=[]

                    besoinNvClavier=True #Pour cree un nouveau (objet) clavier,comme l'ancien a été colore pendant le jeu

                    # on génére un nouveau mot à deviner
                    ANSWER=random.choice(WORDS)
                    SaveSession(sessionpath,data,ANSWER,score,INPUTS,word_length)
                    
                    ScoreInc = False
                    FIN=False
                
               #Si on clique sur ENTRER
                if event.key == pygame.K_RETURN :
                    if M_INPUT.lower() in WORDS: #on vérifie si le mot est correcte
                        if len(M_INPUT)==word_length  :
                            
                            INPUTS.append(M_INPUT) #on ajout le mots à la liste des tentatives
                            
                            if M_INPUT == ANSWER.upper() : #si le mot entré est le mot rechercher on met fin au jeu
                                FIN = True
                                
                            M_INPUT=""
                            SaveSession(sessionpath,data,ANSWER,score,INPUTS,word_length)

                    else: #si le mot entré n'est pas correcte
                            toBeRed=True
                        
                #detection de lettre entrer par clavier du Computer
                if len(INPUTS) < 6 and len(M_INPUT)<word_length and not FIN :
                    if event.unicode.upper().isalpha():
                        M_INPUT = M_INPUT + event.unicode.upper()
                
        pygame.time.Clock().tick(60)
        pygame.display.flip()

        #si le joueur entre le mot vocalement
        if not clavier.inputFromMicQueue.empty():
                clavier.intermediateBtnClavier_clicked=False
                # on extrait le mot inséré par micro
                response=clavier.inputFromMicQueue.get()

                if(response["success"]): 
                    result=response["transcription"]
                    print(result)
                    if len(result)==clavier.word_length:
                        M_INPUT=result.upper()
                        
                else:
                    print(response["error"])
    
    #---------------------------------------------------------------------------------------------------
    interfaceDecider()  
