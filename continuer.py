def continuer():
    import pygame
    from assets import Button
    from assets import Toggle
    import os
    import json
    from quit import quitInterface,takeBluredScreenshot
    #-----------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------
    from fonctions import addToList
    from fonctions import removeFromList
    from fonctions import interfaceDecider

    from session_functions import DelAttempts
    from session_functions import SaveSession
    
    from game import game
    #-----------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------



    os.system("cls")
    directory=os.path.dirname(__file__)
    print(directory)                                    #making the directory of the session file
    sessionpath = directory+"/game_session.json"


    f = open(sessionpath,"r")             #loading session file
    data = json.load(f)
    f.close()

    pygame.init()
    pygame.font.init()

    RED =(233, 53, 53)
    OUR_BLACK =(33, 33, 33)
    BTN_GREY =(196, 196, 196)
    HOVER_GREY =(114,114,114)
    GRIS=(120, 124, 126)
    VERT=(106, 170, 100)
    JAUNE=(201, 180, 88)
    WHITE =(255,255,255)

    mode="Dark"
    # if mode=="Light" :
    #     bgColor=WHITE
    #     carre_color=BTN_GREY 
    #     lettre_color=GRIS
    #     color_interne=WHITE
                        
    # elif mode=="Dark" :
    #     bgColor=OUR_BLACK
    #     carre_color=BTN_GREY 
    #     lettre_color=OUR_BLACK
    #     color_interne=OUR_BLACK

    #Dimensions
    HIGHT=630
    WEIGHT=425
    # TOP_MARGIN=70
    # BUTTOM_MARGIN=150
    # LR_MARGIN=50
    # BETWEEN=5


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
        textColor=COLORS["OUR_BLACK"]
        btnTextColor=COLORS["WHITE"]
        btnColor=COLORS["HOVER_GREY"]
        btnColorHover=COLORS["BTN_GREY"]
    #-------------------

    #SCREEN
    SCREEN=pygame.display.set_mode([WEIGHT,HIGHT])

    #BUTTONS
    cont = Button(TXT["cont_cont"], (WEIGHT/2-(100),150),bodyColor=btnColor,textColor=btnTextColor)
    new_game = Button(TXT["cont_new"], (WEIGHT/2-(100),225),bodyColor=btnColor,textColor=btnTextColor)

    #back icon
    continue_back = Button("",imagepath=directory+r"\assets\arrowFor"+mode+".svg",position=(10,10))

    #text
    font = pygame.font.Font(None, 35)
    text = font.render(TXT["cont_word"], True, textColor)
    text_rect = text.get_rect(center=(WEIGHT/2, 350))

    five = font.render("5", True, textColor)
    five_rect = five.get_rect(center=(WEIGHT/2 - 50 , 400))

    six = font.render("6", True, textColor)
    six_rect = six.get_rect(center=(WEIGHT/2 + 50 , 400))

    toggleBtn=Toggle([WEIGHT/2 - 25 , 400 - 20],16,borderColor=btnColor,color=btnColor,left=not data["lengthsix"])
    # toggleBtn.left=data["lengthsix"]
    # if(data["lengthsix"]):
    #     toggleBtn.left = False                                      #the toggle's direction depends on the length on json file (if six right if five left)
    lensix =  (len(data["guess"])==6)                                    #saves the length of the actual session because it will be modified with clicks (look at line 166)


    run=True
    while run:
        SCREEN.fill(bgColor)
        if (lensix == toggleBtn.left) or (data["score"]==0 and data["attempt0"]==""):
            Button(TXT["cont_cont"], (WEIGHT/2-(100),150), textColor=btnTextColor, bodyColor=btnColorHover).render(SCREEN)
        else:
            cont.render(SCREEN)

        new_game.render(SCREEN)
        toggleBtn.render(SCREEN)
        continue_back.render(SCREEN)
        SCREEN.blit(text, text_rect)
        SCREEN.blit(five, five_rect)
        SCREEN.blit(six, six_rect)
        # data["lengthsix"] = (not toggleBtn.left)

        if cont.hovered():
            Button(TXT["cont_cont"], (WEIGHT/2-(100),150), textColor=btnTextColor, bodyColor=btnColorHover).render(SCREEN)
        
        if new_game.hovered():
            Button(TXT["cont_new"], (WEIGHT/2-(100),225), textColor=btnTextColor, bodyColor=btnColorHover).render(SCREEN)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                takeBluredScreenshot(SCREEN)
                addToList(quitInterface)
                run=False

  
            if event.type==pygame.MOUSEBUTTONDOWN:
                #back icon
                if cont.clicked():
                    if(lensix == toggleBtn.left) or (data["score"]==0 and data["attempt0"]==""):    #if (length of session changed) or (session empty/no progress yet)
                        print("can't continue")
                    else:
                        addToList(game)
                        run = False

                if continue_back.clicked():
                    removeFromList()
                    run=False
                #new_game
                if new_game.clicked():
                    if(data["lengthsix"]):                                                  #creates new session depending on the new length (defined by the toggle)
                        SaveSession(sessionpath,data,"",0,["","","","","",""],6)
                    else:
                        SaveSession(sessionpath,data,"",0,["","","","","",""],5)

                    addToList(game)
                    run=False

                if toggleBtn.clicked():
                    if data["lengthsix"]:                                                                                               #inverts the length
                        # data["lengthsix"] = False
                        templen = 5
                    else:
                        # data["lengthsix"] = True
                        templen = 6
                    SaveSession(sessionpath,data,data["guess"],data["score"],[data["attempt"+str(i)] for i in range(0,6)],templen)  #overwrites the json file
    


                    
        pygame.time.Clock().tick(60)
        pygame.display.flip()
    
    #----------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------
    interfaceDecider()
    #----------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------

# if __name__=="__main__":
#     continuer()