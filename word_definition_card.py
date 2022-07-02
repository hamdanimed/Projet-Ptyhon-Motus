
import pygame
import os


directory=os.path.dirname(__file__)


def takeBluredScreenshot(SCREEN):
    '''cette fonction permet de prendre screenshot floue de l'interface precedente'''
    from PIL import Image,ImageFilter #PIL module utilisé pour prendre une image floue de l'interface courante

    #size:la taile de l'image floue.
    #image_mode est le mode utilisé pour rendre l'image floue(32-bit image with an alpha channel)
    #raw contient l'image de l'interface sous forme string
    size, image_mode, raw = (SCREEN.get_width(), SCREEN.get_height()), 'RGBA', pygame.image.tostring(SCREEN,"RGBA")

    # creer un objet image PIL et rendre l'image floue en le filter GaussianBlur
    pil_blured = Image.frombytes(image_mode, size, raw).filter(ImageFilter.GaussianBlur(radius=2))
    
    # sauvegarder l'image floue pour l'accéder dans l'interface quit (quitInterface fonction)
    pil_blured.save(directory+r"/assets/blur.png")



def drawText(surface,text,color, rect, font, antialiasing=True, bkg=None):
    '''cette fonction permet la mise en forme d'un texte dans un espace limité'''
    rect = pygame.rect.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # la longueur de la police
    fontHeight = font.size("text")[1]
    
    while text:
        i = 1

        # determiner si la ligne de texte va etre à l'exterieur de l'espace
        if y + fontHeight > rect.bottom:
            break

        
        # determiner la largeur maximale de la ligne
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # si on saute la ligne ,alors on ajuste le saut tel que on ne divise pas un mot      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        #dessiner la line dans la surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], antialiasing, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        #supprimer le texte déjà dessiné
        text = text[i:]

    




def getWordDefinition(word,queue):
    import requests                 #module utilisé pour envoyer des HTTP requetes à l'api de definition du mot
    from colors import getLangue    #fonction utiliser pour avoir la langue choisie
    language=getLangue()
    word=word.lower()
    if(language == "en"):
        #lien de l'api dictionnaire en anglais
        link=f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        try:
            req=requests.get(link) #envoyer a GET request à l'api pour avoir la definition
            if(req.status_code == 200):
                #si  HTTP status code est 200
                data=req.json()
                #on extrait une definition       
                definition=word+" : "+data[0]['meanings'][0]['definitions'][0]['definition']
                queue.put(definition)
            else:
                definition="Sorry something went wrong try later.check your connection."
                queue.put(definition)

        
        #si api est introuvable ou erreur de connexion
        except requests.ConnectionError:
            return "Sorry something went wrong try later.check your connection."
    if(language == "fr"):
        #lien de l'api dictionnaire en anglais
        link=f"https://frenchwordsapi.herokuapp.com/api/WordDefinition?idOrName={word}"
        try:
            req=requests.get(link) #envoyer a GET request à l'api pour avoir la definition
            if(req.status_code == 200):
                #si  HTTP status code est 200
                data=req.json()
                #on extrait une definition       
                definition=data['Definition'][0].removeprefix('1.\xa0')
                definition=word+" : "+definition
                queue.put(definition)
            else:
                definition="désolé une erreur s'est produite."
                queue.put(definition)

        #si api est introuvable ou erreur de connexion
        except requests.ConnectionError:
            definition="désolé une erreur s'est produite."
            queue.put(definition)



    



def definitionInterface()->None:
    from assets import Button
    import json
    from PIL import Image 
    from colors import COLORS
    from fonctions import interfaceDecider
    from fonctions import removeFromList

    pygame.init()
    SCREEN = pygame.display.set_mode([425,630])
    

    #taille et image mode  de l'image floue de l'interface precedente
    size, image_mode = (SCREEN.get_width(), SCREEN.get_height()), 'RGBA'
    #recuperation de l'image floue de l'interface precedente et faire une copie et la stocker dans une variable
    blured_image=Image.open(directory+"/assets/blur.png").copy()
    
    # supprimer le fichier .png qui contient l'image floue
    os.remove(directory+r"/assets/blur.png")
    
    
    # convertir l'image floue en une surface pygame pour la dessiner
    surface=pygame.image.fromstring(blured_image.tobytes("raw", image_mode), size, image_mode)
    

    #taille du cadre de definition
    HEIGHT=210
    WIDTH=341

    #x et y sont l'abscisse et l'ordonné ou on dessine le cadre de definition
    x=SCREEN.get_width()//2 - WIDTH//2
    y=SCREEN.get_height()//2-HEIGHT//2
    
    from colors import getMode
    
    MODE=getMode()

    if(MODE == "dark"):
        card_color=COLORS["OUR_BLACK"]
        textColor=COLORS["WHITE"]
        outline_color=COLORS["WHITE"]
        quitButtonImage="assets/XForDark.svg"

    if(MODE == "light"):
        card_color=COLORS["WHITE"]
        textColor=COLORS["OUR_BLACK"]
        outline_color=COLORS["OUR_BLACK"]
        quitButtonImage="assets/XForLight.svg"


    
    ########le cadre de definition de mot################
    card=pygame.rect.Rect(x,y,WIDTH,HEIGHT)
    
    #######################################

    ####bords de cadre###################
    
    thickness = 2
    posx = card.x - thickness
    posy = card.y - thickness
    sizex = card.size[0] + thickness * 2
    sizey = card.size[1] + thickness * 2

    ########################

    #le rectangle qui contient le texte
    textRect=pygame.rect.Rect(card.topleft[0]+30,card.topleft[1]+30,card.width-60,card.height-30)
    
    #quit bouton
    quitButton=Button("",(card.topright[0]-30,card.topright[1]+4),imagepath=quitButtonImage)
    
    #la definition du mot
    with open(directory+r"/game_session.json","r") as f:
        data=json.load(f)
        wordToGuess=data["guess"]
    
    import queue
    import threading
    from colors import getLangue    #fonction utiliser pour avoir la langue choisie
    language=getLangue()

    inputFromDefQueue=queue.Queue()

    threading.Thread(target=getWordDefinition,args=(wordToGuess,inputFromDefQueue),daemon=True).start()
    if language=="en":
        definition="Waiting for the API..."
    elif(language=="fr"):
        definition="En Attendant l'API..."

    run=True
    while run :
        SCREEN.blit(surface, (0,0))

        pygame.draw.rect(SCREEN,card_color,card)
        pygame.draw.rect(SCREEN,outline_color, (posx, posy, sizex, sizey), thickness,border_radius=3)
        quitButton.render(SCREEN)
        drawText(SCREEN,definition,textColor,textRect,pygame.font.SysFont(pygame.font.get_default_font(),30))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #si on clique sur le X bouton on retourne à l'interface precedente
                if quitButton.clicked():
                    sessionpath = directory+"\game_session.json"
                    with open(sessionpath,'w') as f2:
                        data["guess"] = ""          #on supprime le mot déjà recherché du fichier session
                        json.dump(data,f2)
                    removeFromList()   #supprimer l'interface quitter de la liste qui gère les interfaces
                    run=False
        

        if not inputFromDefQueue.empty():
                    definition=inputFromDefQueue.get()
                    # print(definition)
    
        pygame.time.Clock().tick(60)
        pygame.display.flip()

    interfaceDecider()   #on retourne à l'interface precedente si la boucle des evenements est terminée
    
    
    
    
    





