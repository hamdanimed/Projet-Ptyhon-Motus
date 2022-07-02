import pygame
import os
directory=os.path.dirname(__file__)


def takeBluredScreenshot(SCREEN):
    from PIL import Image,ImageFilter #PIL module utilisé pour prendre une image floue de l'interface courante

    #size:la taile de l'image floue.
    #image_mode est le mode utilisé pour rendre l'image floue(32-bit image with an alpha channel)
    #raw contient l'image de l'interface sous forme string
    size, image_mode, raw = (SCREEN.get_width(), SCREEN.get_height()), 'RGBA', pygame.image.tostring(SCREEN,"RGBA")

    # creer un objet image PIL et rendre l'image floue en le filter GaussianBlur
    pil_blured = Image.frombytes(image_mode, size, raw).filter(ImageFilter.GaussianBlur(radius=2))
    
    # sauvegarder l'image floue pour l'accéder dans l'interface quit (quitInterface fonction)
    pil_blured.save(directory+r"/assets/blur.png")




def quitInterface():
    from assets import Button   
    from colors import COLORS
    import sys
    from PIL import Image
    import os
    
    ########### LINKING CODE####################
    from fonctions import removeFromList    #pour supprimer une interface de la liste qui gere les evenements 
    from fonctions import interfaceDecider  # pour lancer l'interface
    
    ##################################

    pygame.init()
    # initialisation de l'interface 
    SCREEN = pygame.display.set_mode([425,630]) 

    #taille et image mode  de l'image floue de l'interface precedente
    size, image_mode = (SCREEN.get_width(), SCREEN.get_height()), 'RGBA'
    #recuperation de l'image floue de l'interface precedente et faire une copie et la stocker dans une variable
    blured_image=Image.open(directory+"/assets/blur.png").copy()
    
    # supprimer le fichier .png qui contient l'image floue
    os.remove(directory+r"/assets/blur.png")
    
    
    # convertir l'image floue en une surface pygame pour la dessiner
    surface=pygame.image.fromstring(blured_image.tobytes("raw", image_mode), size, image_mode) 
    

    #taille du cadre quitter
    HEIGHT=210
    WIDTH=341

    #x et y sont l'abscisse et l'ordonné ou on dessine le cadre quitter
    x=SCREEN.get_width()//2 - WIDTH//2
    y=SCREEN.get_height()//2-HEIGHT//2
    
    #------le dictionnaire utilisé pour le changemment de langue-------#
    
    from colors import getTXT

    TXT=getTXT() #le dictionnaire avec les mots affiché , utilise pour changement de langue 
    #------------------------------------------------------------#



    from colors import getMode #pour savoir quel mode on utilise dark ou light mode
    
    MODE=getMode()

    if(MODE == "dark"):
        card_color=COLORS["OUR_BLACK"]      #couleur du cadre quitter
        textColor=COLORS["WHITE"]           #couleur du texte du cadre quitter
        outline_color=COLORS["WHITE"]       #couleur de bords du cadre quitter
        btnTextColor=COLORS["OUR_BLACK"]    #couleur du texte des boutons
        btnColor=COLORS["BTN_GREY"]         #couleur des boutons
        btnColorHover=COLORS["HOVER_GREY"]  #couleur du survol des boutons
        
        
    if(MODE == "light"):
        card_color=COLORS["WHITE"]          #couleur du cadre quitter
        textColor=COLORS["OUR_BLACK"]       #couleur du texte du cadre quitter
        outline_color=COLORS["OUR_BLACK"]   #couleur de bords du cadre quitter
        btnTextColor=COLORS["WHITE"]        #couleur du texte des boutons
        btnColor=COLORS["HOVER_GREY"]       #couleur des boutons
        btnColorHover=COLORS["BTN_GREY"]    #couleur du survol des boutons
        


    ########  cadre quitter ################
    card=pygame.rect.Rect(x,y,WIDTH,HEIGHT)
    
    #######################################

    ####bords du cadre quitter###################
    
    thickness = 2
    posx = card.x - thickness
    posy = card.y - thickness
    sizex = card.size[0] + thickness * 2
    sizey = card.size[1] + thickness * 2
    

    ########################

    #le texte qui contient voulez vous vraiment quitter
    text=pygame.font.SysFont("",35).render(TXT["quit_sure1"],True,textColor)
    text2=pygame.font.SysFont("",35).render(TXT["quit_sure2"],True,textColor)
    textRect=text.get_rect(topleft=(card.topleft[0]+30,card.topleft[1]+card.height//2-55))
    textRect2=text2.get_rect(topleft=(card.topleft[0]+30,card.topleft[1]+card.height//2-25))
    


    #X bouton
    quitButton=Button("x",(card.topright[0]-30,card.topright[1]+7),size=(25,25),textSize=90,bodyColor=btnColor,textColor=btnTextColor)
    

    #Quit motus / Quitter bouton
    quitMotusButton=Button(TXT["quit_quit"],(card.bottomright[0]-300,card.bottomright[1]-80),size=(140,40),textSize=60,bodyColor=btnColor,textColor=btnTextColor)
    
    
    #Cancel / Annuler bouton
    cancelButton=Button(TXT["quit_cancel"],(card.bottomright[0]-135,card.bottomright[1]-80),size=(90,40),textSize=60,bodyColor=btnColor,textColor=btnTextColor)

    run=True
    #la boucle des evenements eventloop
    while run:
        # dessiner l'interface pygame qui contient l'image floue de l'interface precedente
        SCREEN.blit(surface, (0,0)) 
        
        # dessiner le cadre quitter en dessus de l'image floue
        pygame.draw.rect(SCREEN,card_color,card)
        pygame.draw.rect(SCREEN,outline_color, (posx, posy, sizex, sizey), thickness,border_radius=3)
        SCREEN.blit(text,textRect)
        SCREEN.blit(text2,textRect2)
        ###################
        

        # dessiner les boutons
        cancelButton.render(SCREEN)
        quitMotusButton.render(SCREEN)
        quitButton.render(SCREEN)

        # changer le couleur des boutons en cas de survol
        if quitButton.hovered():
            Button("x",(card.topright[0]-30,card.topright[1]+7),size=(25,25),textSize=90,textColor=(255,255,255),bodyColor=(255,0,0)).render(SCREEN)
        if quitMotusButton.hovered():
            Button(TXT["quit_quit"],(card.bottomright[0]-300,card.bottomright[1]-80),size=(140,40),textSize=60,bodyColor=btnColorHover,textColor=btnTextColor).render(SCREEN)
        if cancelButton.hovered():
            Button(TXT["quit_cancel"],(card.bottomright[0]-135,card.bottomright[1]-80),size=(90,40),textSize=60,bodyColor=btnColorHover,textColor=btnTextColor).render(SCREEN)



        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #si on clique sur le bouton cancel (annuler) ou  X bouton on retourne à l'interface precedente
                if cancelButton.clicked() or quitButton.clicked():
                    removeFromList()  #supprimer l'interface quitter de la liste qui gère les interfaces
                    run=False
                #si on clique sur le bouton Quit Motus (Quitter) on arrete le jeu
                if quitMotusButton.clicked():
                    pygame.quit()
                    sys.exit()
                    

        pygame.time.Clock().tick(60)
        
        pygame.display.flip()
                

    interfaceDecider()  #on retourne à l'interface precedente si la boucle des evenements est terminée