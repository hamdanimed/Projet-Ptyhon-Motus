import pygame
import os
directory=os.path.dirname(__file__)

# var={"0":True}

# lang={"0":True}

GREEN =(67, 205, 55)
YELLOW =(212, 216, 40)
RED =(233, 53, 53)
BLACK =(0,0,0)
WHITE =(255,255,255)
OUR_BLACK =(33, 33, 33)
BTN_GREY =(196, 196, 196)
HOVER_GREY =(114,114,114)

def pointInRectanlge(px, py, rw, rh, rx, ry):
    if px > rx and px < rx  + rw:
        if py > ry and py < ry + rh:
            return True
    return False

class Toggle:
    def __init__(self,position,circleRadius=16,color=WHITE,borderColor=BTN_GREY,left=True) -> None:
        
        self.pos=position
        self.color=color
        self.left=left
        self.borderThickness=3
        self.borderColor=borderColor
        self.disappearColor=OUR_BLACK

        self.circleRadius=circleRadius
        self.width=self.circleRadius*2+self.borderThickness*2+14
        self.height=self.circleRadius*2+self.borderThickness*2
        self.leftCirclePos=[int(self.width/2-7),int(self.height/2)]
        self.rightCirclePos=[int(self.width/2+7),int(self.height/2)]
        
        
        self.surface=pygame.Surface((self.width,self.height)).convert()
        self.surface.fill(self.disappearColor)

    def clicked(self):
        mousePos = pygame.mouse.get_pos()
        if pointInRectanlge(mousePos[0], mousePos[1], self.width, self.height, self.pos[0], self.pos[1]):
                self.left=not self.left
                # print("clicked",self.left) 
                return True
    
    def render(self,window):
        
        window.blit(self.surface, (self.pos[0],self.pos[1]))
        self.surface.set_colorkey(self.disappearColor)
        # border
        pygame.draw.rect(window,self.borderColor, (self.pos[0] + self.width/2 - self.width/2, self.pos[1] + self.height/2 - self.height/2, self.width, self.height), self.borderThickness,border_radius=self.circleRadius*2)

        if self.left:
            pygame.draw.circle(self.surface,self.disappearColor,self.rightCirclePos, self.circleRadius, 0) 
            pygame.draw.circle(self.surface,self.color,self.leftCirclePos, self.circleRadius, 0) 
        else :
            pygame.draw.circle(self.surface,self.disappearColor,self.leftCirclePos, self.circleRadius, 0)
            pygame.draw.circle(self.surface,self.color,self.rightCirclePos, self.circleRadius, 0)

        # if eventClick:
        #     if pointInRectanlge(mousePos[0], mousePos[1], self.width, self.height, self.pos[0], self.pos[1]):
        #         if eventClick == pygame.MOUSEBUTTONDOWN :
        #             self.left=not self.left
        #             print("clicked",self.left) 

class Button:

    def __init__(self, text:str, position:tuple,bodyColor=(196, 196, 196),textColor=(33, 33, 33), size:tuple=(200, 50),textSize=50,outline:bool=False,imagepath=None)->None:
        self.position = position
        self.size = size
        self.bodyColor=bodyColor
        self.button = pygame.Rect(position,size)
        self.outline = outline
        self.textColor=textColor
        self.txt=text
        font = pygame.font.Font(directory+"\\assets\\font\istok Web\IstokWeb-Bold.ttf", int((textSize/100)*self.size[1]))
        self.textSurf = font.render(f"{self.txt}", True, self.textColor)
        self.image=None
        if(imagepath):
            self.image=pygame.image.load(os.path.join(directory,imagepath))
            self.button=self.image.get_rect(topleft=self.position)


    def clicked(self)->bool:
        mousePos = pygame.mouse.get_pos()
        if self.button.collidepoint(mousePos[0], mousePos[1]):
                return True   
        return False

    def hovered(self)->None:
        mousePos = pygame.mouse.get_pos()
        if self.button.collidepoint((mousePos[0],mousePos[1])):
            return True
        return False

    def changeText(self,txt):
        self.txt=txt
    
    def render(self, display:pygame.display)->None:
        
        if(self.image == None):
            textx = self.position[0] + (self.button.width/2) - (self.textSurf.get_rect().width/2)
            texty = self.position[1] + (self.button.height/2) - (self.textSurf.get_rect().height/2)
            
            #display button first then text
            pygame.draw.rect(display,self.bodyColor,self.button,border_radius=2)
            display.blit(self.textSurf, (textx, texty))
            
            if self.outline:
                outlineColor=GREEN
                thickness = 2
                posx = self.position[0] - thickness
                posy = self.position[1] - thickness
                sizex = self.size[0] + thickness * 2
                sizey = self.size[1] + thickness * 2

                

                pygame.draw.rect(display,outlineColor, (posx, posy, sizex, sizey), thickness,border_radius=3)
        else:
            
            display.blit(self.image,self.button)



def checkword(WORDTOGUESS,guess,V,Y,G):

    
    length=len(WORDTOGUESS)
    WORDTOGUESS=WORDTOGUESS.lower()

    
    response=[G for _ in range(length)]
    guess=guess.lower()
    yellow_dark_positions=[]
    for i in range(length):
        if(WORDTOGUESS[i] == guess[i]):
            response[i]=V
        else:
            yellow_dark_positions.append(i)
    
    word2=[]
    for i in yellow_dark_positions:
        word2.append(WORDTOGUESS[i])

    for i in yellow_dark_positions:
        if(guess[i] in word2):
            response[i]=Y
            word2.remove(guess[i])
    # print(response)
    return response