def about():
    from assets import Button   #importer la classe button
    import pygame               #importer le module Pygame
    from quit import quitInterface,takeBluredScreenshot
    
    #---- Importer le module OS pour gerer les chemins des fichiers ----#
    import os
    directory=os.path.dirname(__file__)
    print(directory)
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

    TXT=getTXT() #le dictionnaire avec les mots affiche , utilise pour changement entre les langues
    #------------------------------------------------------------#


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

    #.................... le texte de jeu MOTUS .....................#

    # TITRE_ABOUT
    LANGUAGE_TEXT = pygame.font.Font(os.path.join(directory,r"assets\font\istok web\IstokWeb-Bold.ttf"),70).render(TXT["about_about"], True, textColor)
    # pour définir où on veut mettre le texte_1
    LANGUAGE_RECT = LANGUAGE_TEXT.get_rect(center=(200, 150))
    
    # TEXT_1
    LANGUAGE_TEXT1 = pygame.font.Font(os.path.join(directory,r"assets\font\istok web\IstokWeb-Bold.ttf"),15).render(TXT["about_txt1"], True, textColor)
    LANGUAGE_TEXT2 = pygame.font.Font(os.path.join(directory,r"assets\font\istok web\IstokWeb-Bold.ttf"),15).render(TXT["about_txt2"], True, textColor)
    LANGUAGE_TEXT3 = pygame.font.Font(os.path.join(directory,r"assets\font\istok web\IstokWeb-Bold.ttf"),15).render(TXT["about_txt3"], True, textColor)
    # pour définir où on veut mettre le texte_1
    LANGUAGE_RECT1 = LANGUAGE_TEXT1.get_rect(center=(205, 200))
    LANGUAGE_RECT2 = LANGUAGE_TEXT2.get_rect(center=(205, 220))
    LANGUAGE_RECT3 = LANGUAGE_TEXT3.get_rect(center=(205, 240))

    # TEXT_2
    LANGUAGE_INFO1 = pygame.font.Font(os.path.join(directory,r"assets\font\istok web\IstokWeb-Bold.ttf"),15).render(TXT["about_rul1"], True, textColor)
    LANGUAGE_INFO2 = pygame.font.Font(os.path.join(directory,r"assets\font\istok web\IstokWeb-Bold.ttf"),15).render(TXT["about_rul2"], True, textColor)
    LANGUAGE_INFO3 = pygame.font.Font(os.path.join(directory,r"assets\font\istok web\IstokWeb-Bold.ttf"),15).render(TXT["about_rul3"], True, textColor)
    LANGUAGE_INFO4 = pygame.font.Font(os.path.join(directory,r"assets\font\istok web\IstokWeb-Bold.ttf"),15).render(TXT["about_rul4"], True, textColor)
    # pour définir où on veut mettre le texte_2
    LANGUAGE_RECT_INFO1 = LANGUAGE_INFO1.get_rect(topleft=(65, 290))
    LANGUAGE_RECT_INFO2 = LANGUAGE_INFO2.get_rect(topleft=(66, 340))
    LANGUAGE_RECT_INFO3 = LANGUAGE_INFO3.get_rect(topleft=(66, 390))
    LANGUAGE_RECT_INFO4 = LANGUAGE_INFO4.get_rect(topleft=(66, 440))
    #..................................................................#


    #----------------- les bouton de l'interface ------------------#
    BACK=Button(text="",imagepath=os.path.join(directory,r".\assets\arrowForDark.svg"),position=(16,13),textColor=textColor)
    #--------------------------------------------------------------#



    #------------- La boucle de pygame pour dessiner l'élément créé à l'écran -------------#
    run=True
    while run:
        SCREEN.fill(bgColor)

        #....................la methode blit pour dessiner les Buttons ......................#
        SCREEN.blit(pygame.image.load(os.path.join(directory,r"assets\green.png")),(18,282))
        SCREEN.blit(pygame.image.load(os.path.join(directory,r"assets\r.png")),(18,432))
        SCREEN.blit(pygame.image.load(os.path.join(directory,r"assets\g.png")),(18,382))
        SCREEN.blit(pygame.image.load(os.path.join(directory,r"assets\y.png")),(18,332))
        #...................................................................#
        

        #---------- dessiner les boutons à l'écran -----------#
        BACK.render(SCREEN)
        #-----------------------------------------------------#


        #----------- dessiner les texte à l'écran ------------#
        # TITRE_ABOUT
        SCREEN.blit(LANGUAGE_TEXT, LANGUAGE_RECT)
        # TEXT_1
        SCREEN.blit(LANGUAGE_TEXT1, LANGUAGE_RECT1)
        SCREEN.blit(LANGUAGE_TEXT2, LANGUAGE_RECT2)
        SCREEN.blit(LANGUAGE_TEXT3, LANGUAGE_RECT3)
        # TEXT_2
        SCREEN.blit(LANGUAGE_INFO1, LANGUAGE_RECT_INFO1)
        SCREEN.blit(LANGUAGE_INFO2, LANGUAGE_RECT_INFO2)
        SCREEN.blit(LANGUAGE_INFO3, LANGUAGE_RECT_INFO3)
        SCREEN.blit(LANGUAGE_INFO4, LANGUAGE_RECT_INFO4)
        #-----------------------------------------------------#


        #------- Boucle pour gérer l'événement de cliquant sur les boutons -------#
        for event in pygame.event.get():
                if event.type == pygame.QUIT:   # s'ils cliquent sur Quit, nous appelons l'interface de Quit
                    takeBluredScreenshot(SCREEN)
                    addToList(quitInterface)
                    run=False
                if event.type == pygame.MOUSEBUTTONDOWN:    # s'ils cliquent sur Back, on appel la page précédente
                    if BACK.clicked() :
                        removeFromList()
                        run=False
                        
        pygame.time.Clock().tick(60)    # pour limiter FPS a 60
        pygame.display.update()         # Methode de Pygame pour mettre à jour la fenêtre
    
    
    interfaceDecider()
    

# about()


