def language():
    import pygame, sys          #importer le module Pygame
    from assets import Button   #importer la classe button
    #
    from quit import quitInterface,takeBluredScreenshot

    
    #---- Importer le module OS pour gerer les chemins des fichiers ----#
    import os
    directory=os.path.dirname(__file__)
    #------------------------------------------------------------------#
    
    #-------------les fontions utilises pour lier les interfaces------------#
    from fonctions import addToList
    from fonctions import removeFromList
    from fonctions import interfaceDecider
    #-----------------------------------------------------------------------#
    
    
    #------le dictionnaire utilisé pour le changemment de langue-------#
    from colors import getLangue
    from colors import changeLang
    from colors import getTXT

    langueStart=getLangue()
    TXT=getTXT() #le dictionnaire avec les mots affiche , utilise pour changement entre les langues
    #------le dictionnaire utilisé pour le changemment de mode LIGHT/DARK -------#
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
    #-----------------------------------------------------------------------------#


    #----------------- Initialiser pygame ------------------#
    pygame.init()
    pygame.display.set_caption("MOTUS") 
    #-------------------------------------------------------#


    #initialiser la fenetre du jeu 
    HEIGHT=630
    WIDTH=425
    SCREEN=pygame.display.set_mode((WIDTH,HEIGHT))
    ######################

    #----------------- les bouton de l'interface ------------------#    
    LANGUAGE_ENGLISH = Button(position=(144 ,295),textSize=50,text=TXT["lang_en"], size=(137, 35),bodyColor=btnColor,textColor=btnTextColor)
    LANGUAGE_FRENCH = Button(position=(144 ,357),textSize=50,text=TXT["lang_fr"], size=(137, 35),bodyColor=btnColor,textColor=btnTextColor)
    BACK_BUTTON = Button(text="",imagepath=directory+r"\assets\arrowForDark.svg",position=(16,13))
    #--------------------------------------------------------------#
   

    #.................... le texte de jeu MOTUS .....................#
    LANGUAGE_TEXT = pygame.font.Font(directory+r"/assets/font/istok web/IstokWeb-Bold.ttf",40).render(TXT["lang_lang"], True, textColor)
    LANGUAGE_RECT = LANGUAGE_TEXT.get_rect(center=(212, 180))
    #..................................................................#


    run=True
    while run:

        SCREEN.fill(bgColor)
        #....................la methode blit pour dessiner le text ......................#
        SCREEN.blit(LANGUAGE_TEXT, LANGUAGE_RECT) 
        #...................................................................#


        #---------- dessiner les boutons à l'écran -----------#
        for button in [LANGUAGE_ENGLISH, LANGUAGE_FRENCH, BACK_BUTTON]:  # this boucle to keep the the button on the screen
            button.render(SCREEN)
        #-----------------------------------------------------#
        

        #...................... Flotter/(Hover) les bouton crée ......................#
        if LANGUAGE_ENGLISH.hovered() or getLangue()!="fr":
            Button(position=(144 ,295),textSize=50,text=TXT["lang_en"], size=(137, 35),bodyColor=btnColorHover,textColor=btnTextColor).render(SCREEN)
        
        if LANGUAGE_FRENCH.hovered() or getLangue()!="en":
            Button(position=(144 ,357),textSize=50,text=TXT["lang_fr"], size=(137, 35),bodyColor=btnColorHover,textColor=btnTextColor).render(SCREEN)
        
        #...........................................................................#


        #------- Boucle pour gérer l'événement de cliquant sur les boutons -------#
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:   # s'ils cliquent sur Quit, nous appelons l'interface de Quit
                takeBluredScreenshot(SCREEN)
                addToList(quitInterface)
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LANGUAGE_ENGLISH.clicked() and getLangue()!="en":   # s'ils cliquent sur ENGLISH, on change la langue en Anglais
                    changeLang()
                    run=False
                    
                if LANGUAGE_FRENCH.clicked() and getLangue()!="fr":     # s'ils cliquent sur FRENCH, on change la langue en Francais
                    changeLang()
                    run=False

                if BACK_BUTTON.clicked():   # s'ils cliquent sur Back, on appel la page précédente
                    removeFromList()
                    run=False
                          


        pygame.time.Clock().tick(60)    # pour limiter FPS a 60
        pygame.display.flip()         # Methode de Pygame pour mettre à jour la fenêtre
    
    if langueStart != getLangue():
        from session_functions import SaveSession
        import json
        with open(directory+r"\game_session.json") as f:
            data=json.load(f)
        wordlength= 6 if data["lengthsix"] else 5
        SaveSession(directory+r"\game_session.json",data,"",0,["","","","","",""],wordlength)
    
    ######LINKING CODE########################
    interfaceDecider()
    ######LINKING CODE########################
