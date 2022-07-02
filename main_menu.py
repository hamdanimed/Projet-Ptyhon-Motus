
def main_menu():
    
    from assets import Button   #importer la classe button
    import pygame   #importer le module button

    #---- Importer le module OS pour gerer les chemins des fichiers ----#
    import os    
    directory=os.path.dirname(__file__) 
    #------------------------------------------------------------------#


    #-------importer les interfaces du Jeu ------#
    from continuer import continuer
    from stats import stats
    from about import about
    from language import language
    from quit import quitInterface,takeBluredScreenshot
    #--------------------------------------------#


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
    #-----------------------------------------------------------------------#


    #------le dictionnaire utilisé pour le changemment de mode LIGHT/DARK -------#
    from colors import COLORS
    from colors import changeMode
    from colors import getMode
    
    MODE=getMode()
    if MODE=="dark":
        motusColor=COLORS["BTN_GREY"]
        bgColor=COLORS["OUR_BLACK"]
        btnTextColor=COLORS["OUR_BLACK"]
        btnColor=COLORS["BTN_GREY"]
        btnColorHover=COLORS["HOVER_GREY"]
    elif MODE=="light":
        motusColor=COLORS["HOVER_GREY"]
        bgColor=COLORS["WHITE"]
        btnTextColor=COLORS["WHITE"]
        btnColor=COLORS["HOVER_GREY"]
        btnColorHover=COLORS["BTN_GREY"]
    #-----------------------------------------------------------------------------#


    #----------------- Initialiser pygame ------------------#
    pygame.init() 
    pygame.display.set_caption("MOTUS") 
    ICON = pygame.image.load(directory+"/assets/icon.jpeg")
    pygame.display.set_icon(ICON)
    #-------------------------------------------------------#


    #initialiser la fenetre du jeu 
    HEIGHT=630
    WIDTH=425
    SCREEN=pygame.display.set_mode((WIDTH,HEIGHT))
    ######################
    

    #le texte de jeu MOTUS
    MENU_TEXT = pygame.font.Font(pygame.font.get_default_font(),80).render("MOTUS", True, motusColor)
    MENU_RECT = MENU_TEXT.get_rect(center=(212, 150)) # pour définir où on veut mettre le texte
    #######################


    #----------------- les bouton de l'interface ------------------#
    MODE_BUTTON=Button(text="",imagepath=directory+"/assets/moonForDark.svg",position=(16,16))
    LANGUAGE_BUTTON=Button(text="",imagepath=directory+"\\assets\globeForDark.svg",position=(372,16))
    PLAY_BUTTON = Button(position=(95, 278),text=TXT["main_play"], size=(235, 50),bodyColor=btnColor,textColor=btnTextColor) # Creat the play Button
    STATS_BUTTON = Button(position=(95, 356), text=TXT["main_stats"], size=(235, 50),bodyColor=btnColor,textColor=btnTextColor)  # Creat the Stats Button
    ABOUT_BUTTON = Button(position=(95, 439),text=TXT["main_about"], size=(235, 50),bodyColor=btnColor,textColor=btnTextColor)
    QUIT_BUTTON = Button(position=(95, 522), text=TXT["main_quit"], size=(235, 50),bodyColor=btnColor,textColor=btnTextColor) # Creat the quit Button
    #--------------------------------------------------------------#


    #--------LINKING CODE------------
    done=False
    #--------LINKING CODE------------



    #------------- La boucle de pygame pour dessiner l'élément créé à l'écran -------------#
    SCREEN.fill(bgColor)
    run=True
    while run:

        #....................la methode blit pour dessiner les Buttons ......................#
        SCREEN.blit(MENU_TEXT, MENU_RECT) 
        #...................................................................#


        #---------- dessiner les boutons à l'écran -----------#
        for button in [PLAY_BUTTON, STATS_BUTTON, QUIT_BUTTON,ABOUT_BUTTON,LANGUAGE_BUTTON,MODE_BUTTON]:
            button.render(SCREEN)
        #-----------------------------------------------------#


        #...................... Flotter(hover) les bouton crée ......................#
        if PLAY_BUTTON.hovered() :
            Button(position=(95, 278),text=TXT["main_play"], size=(235, 50),bodyColor=btnColorHover,textColor=btnTextColor).render(SCREEN)
        
        if STATS_BUTTON.hovered() :
            Button(position=(95, 356), text=TXT["main_stats"], size=(235, 50),bodyColor=btnColorHover,textColor=btnTextColor).render(SCREEN)
        
        if ABOUT_BUTTON.hovered() :
            Button(position=(95, 439),text=TXT["main_about"], size=(235, 50),bodyColor=btnColorHover,textColor=btnTextColor).render(SCREEN)
        
        if QUIT_BUTTON.hovered() :
            Button(position=(95, 522), text=TXT["main_quit"], size=(235, 50),bodyColor=btnColorHover,textColor=btnTextColor).render(SCREEN)
        
        #...........................................................................#
        

        #------- Boucle pour gérer l'événement de cliquant sur les boutons -------#
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:# s'ils cliquent sur Quit, nous appelons l'interface de Quit
                takeBluredScreenshot(SCREEN)
                addToList(quitInterface)
                run=False
                # done=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.clicked():   #  s'ils cliquent sur Play, nous appelons l'interface de Play
                    addToList(continuer)
                    run=False
                if STATS_BUTTON.clicked():     # s'ils cliquent sur Stats, nous appelons l'interface de stats
                    addToList(stats)
                    run=False
                if LANGUAGE_BUTTON.clicked():   # s'ils cliquent sur Lanuguage, nous appelons l'interface de language
                    addToList(language)
                    run=False
                if MODE_BUTTON.clicked():   # s'ils cliquent sur Mode, on change le mode Dark/Light
                    changeMode()
                    run=False
                if ABOUT_BUTTON.clicked():   # s'ils cliquent sur About, nous appelons l'interface de About
                    addToList(about)
                    run=False
                if QUIT_BUTTON.clicked():    # s'ils cliquent sur quitter, quiter le jeu
                    removeFromList()
                    done=True
                    run=False


        pygame.time.Clock().tick(60) # pour limiter FPS a 60
        pygame.display.flip() # Methode de Pygame pour mettre à jour la fenêtre

    if not done:
        interfaceDecider()

    #-------------.-----------------------------------------------------.-------------#


if __name__=="__main__":
    from fonctions import interfaceDecider
    interfaceDecider()

