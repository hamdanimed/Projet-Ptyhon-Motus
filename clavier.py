from assets import Button
# from colors import getMode
import pygame
import queue
import threading


import speech_recognition as sr
from speech_recognizer import recognize_speech_from_mic 
from colors import COLORS

# from motus_light import SaveSession
# from motus_light import ANSWER
# from motus_light import FIN
# from motus_light import INPUTS

#Dimensions
HEIGHT=630
WIDTH=425
TOP_MARGIN=70
BUTTOM_MARGIN=150
LR_MARGIN=58
BETWEEN=5
CLAVIER_LR_MARGIN=25
CLAVIER_BUTTOM_MARGIN=HEIGHT-BUTTOM_MARGIN-20 #BUTTOM_MARGIN=150


ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

class Clavier:
    def __init__(self,word_length,FONT_END,MODE):#creation de clavier , utilisant class Button pour chaque button de clavier
        self.word_length=word_length
        self.carre_size_clavier=(WIDTH-2*CLAVIER_LR_MARGIN-10*BETWEEN-32) // 10
        #les buttons qui concerne les lettres
        self.clavierRow1=[Button(ALPHABET[0][i], (CLAVIER_LR_MARGIN+(self.carre_size_clavier+BETWEEN)*(i), CLAVIER_BUTTOM_MARGIN ),size=(self.carre_size_clavier,self.carre_size_clavier+10)) for i in range(10)]
        self.clavierRow2=[Button(ALPHABET[1][i], (CLAVIER_LR_MARGIN+(self.carre_size_clavier/2)+(self.carre_size_clavier+BETWEEN)*(i), CLAVIER_BUTTOM_MARGIN +(self.carre_size_clavier+BETWEEN+10)*1),size=(self.carre_size_clavier,self.carre_size_clavier+10)) for i in range(9)]
        self.clavierRow3=[Button(ALPHABET[2][i], (CLAVIER_LR_MARGIN+(self.carre_size_clavier*1.5+BETWEEN)+(self.carre_size_clavier+BETWEEN)*(i), CLAVIER_BUTTOM_MARGIN +(self.carre_size_clavier+BETWEEN+10)*2),size=(self.carre_size_clavier,self.carre_size_clavier+10)) for i in range(7)]
        #creation de btn pour placer l'icon de audio pour speechRecognition (considere comme btn de premier line)
        self.clavierRow1.insert(len(self.clavierRow1),Button("mic", (CLAVIER_LR_MARGIN+4+(self.carre_size_clavier+BETWEEN)*(10), CLAVIER_BUTTOM_MARGIN+(self.carre_size_clavier+10+BETWEEN)+2 ),size=(self.carre_size_clavier,(self.carre_size_clavier+10)*3+2*BETWEEN),imagepath=r"assets/voiceForDark.svg"))
        #creation de intermediateBtnClavier pour construire le arriere plan de l'image
        self.intermediateBtnClavier=Button("", (CLAVIER_LR_MARGIN+(self.carre_size_clavier+BETWEEN)*(10), CLAVIER_BUTTOM_MARGIN ),size=(self.carre_size_clavier,(self.carre_size_clavier+10)*3+2*BETWEEN))
        # creation de btn Enter
        self.clavierRow3.insert(0,Button("Enter", (CLAVIER_LR_MARGIN, CLAVIER_BUTTOM_MARGIN +(self.carre_size_clavier+BETWEEN+10)*2),size=(self.carre_size_clavier*1.5,self.carre_size_clavier+10),textSize=40))
        #creation de btn delete
        self.clavierRow3.insert(len(self.clavierRow3),Button("del", (CLAVIER_LR_MARGIN+(self.carre_size_clavier*1.5+BETWEEN)+(self.carre_size_clavier+BETWEEN)*(7), CLAVIER_BUTTOM_MARGIN +(self.carre_size_clavier+BETWEEN+10)*2),size=(self.carre_size_clavier*1.5,self.carre_size_clavier+10)))
        #la pile qui va contenir la reponse venue de l'api de speech recognition
        self.inputFromMicQueue=queue.Queue()
        
        self.intermediateBtnClavier_clicked=False
        self.font=FONT_END
        if MODE=="light":
            self.audio_text=FONT_END.render("RECORDING",True,COLORS["OUR_BLACK"])
        elif(MODE=="dark"):
            self.audio_text=FONT_END.render("RECORDING",True,COLORS["BTN_GREY"])
        

    def renderClavier(self,SCREEN):

        #Render de RECORDING
        if self.intermediateBtnClavier_clicked==True:
            # self.audio_text=FONT_END.render("RECORDING",True,COLORS["OUR_BLACK"])
            surface=self.audio_text.get_rect(center=(WIDTH/2,HEIGHT-20))
            SCREEN.blit(self.audio_text,surface)

        for i in range(len(self.clavierRow1)):

            if i != len(self.clavierRow1)-1:
                
                if self.clavierRow1[i].hovered():
                    Button(ALPHABET[0][i], (CLAVIER_LR_MARGIN+(self.carre_size_clavier+BETWEEN)*(i), CLAVIER_BUTTOM_MARGIN ),size=(self.carre_size_clavier,self.carre_size_clavier+10),outline=True).render(SCREEN)
                
                self.clavierRow1[i].render(SCREEN)
            else:

                self.intermediateBtnClavier.render(SCREEN)
                if self.intermediateBtnClavier.hovered():
                    Button("", (CLAVIER_LR_MARGIN+(self.carre_size_clavier+BETWEEN)*(10), CLAVIER_BUTTOM_MARGIN ),size=(self.carre_size_clavier,(self.carre_size_clavier+10)*3+2*BETWEEN),outline=True).render(SCREEN)
                self.clavierRow1[i].render(SCREEN)
                
            


        for i in range(len(self.clavierRow2)):
            
            if self.clavierRow2[i].hovered():
                Button(ALPHABET[1][i], (CLAVIER_LR_MARGIN+(self.carre_size_clavier/2)+(self.carre_size_clavier+BETWEEN)*(i), CLAVIER_BUTTOM_MARGIN +(self.carre_size_clavier+BETWEEN+10)*1),size=(self.carre_size_clavier,self.carre_size_clavier+10),outline=True).render(SCREEN)
            self.clavierRow2[i].render(SCREEN)

                    
        for i in range(len(self.clavierRow3)):

            if self.clavierRow3[i].hovered():
                if i==0:
                    Button("Enter", (CLAVIER_LR_MARGIN, CLAVIER_BUTTOM_MARGIN +(self.carre_size_clavier+BETWEEN+10)*2),size=(self.carre_size_clavier*1.5,self.carre_size_clavier+10),textSize=40,outline=True).render(SCREEN)
                elif (i==len(self.clavierRow3)-1):
                    Button("del", (CLAVIER_LR_MARGIN+(self.carre_size_clavier*1.5+BETWEEN)+(self.carre_size_clavier+BETWEEN)*(7), CLAVIER_BUTTOM_MARGIN +(self.carre_size_clavier+BETWEEN+10)*2),size=(self.carre_size_clavier*1.5,self.carre_size_clavier+10),outline=True).render(SCREEN)
                else:
                    k=i-1
                    Button(ALPHABET[2][k], (CLAVIER_LR_MARGIN+(self.carre_size_clavier*1.5+BETWEEN)+(self.carre_size_clavier+BETWEEN)*(k), CLAVIER_BUTTOM_MARGIN +(self.carre_size_clavier+BETWEEN+10)*2),size=(self.carre_size_clavier,self.carre_size_clavier+10),outline=True).render(SCREEN)
            self.clavierRow3[i].render(SCREEN)
    
    def clickHandler(self,INPUTS,M_INPUT,FIN,ANSWER):
        toSave=False
        
        
        if self.intermediateBtnClavier.clicked():
            self.intermediateBtnClavier_clicked=True

            #on lance le thread de speech recognition
            threading.Thread(target=recognize_speech_from_mic,args=(sr.Recognizer(),sr.Microphone(),self.inputFromMicQueue),daemon=True).start()
          
            
            # if(response["success"]):
            #     result=response["transcription"]
            #     print(result)
            #     if len(result)==self.word_length:
            #         M_INPUT=result.upper()
            # else:
            #     print(response["error"])
                # ERROR=FONT_END.render(response["error"],True,textColor)
                # SCREEN.blit(ERROR,(HEIGHT-20,WIDTH/2))
                    
        for i in range(len(self.clavierRow1)):

            
            if self.clavierRow1[i].clicked():
                
                if len(M_INPUT)<self.word_length and len(INPUTS) < 6 and  not FIN :
                    if self.clavierRow1[i].txt.isalpha() and self.clavierRow1[i].txt !="mic":
                        M_INPUT = M_INPUT + self.clavierRow1[i].txt
                
                
                
                
                
            



        for i in range(len(self.clavierRow2)):
            
            if self.clavierRow2[i].clicked():
                if len(M_INPUT)<self.word_length and len(INPUTS) < 6 and not FIN :
                    if self.clavierRow2[i].txt.isalpha():
                        M_INPUT = M_INPUT + self.clavierRow2[i].txt
            
                    
        for i in range(len(self.clavierRow3)):
            
            if self.clavierRow3[i].clicked():

                if len(M_INPUT)<self.word_length and len(INPUTS) < 6 and i!=len(self.clavierRow3)-1 and  not FIN :
                    if self.clavierRow3[i].txt.isalpha() and self.clavierRow3[i].txt!="Enter":
                        M_INPUT = M_INPUT + self.clavierRow3[i].txt
                if self.clavierRow3[i].txt=="Enter":
                    #if M_INPUT.lower() in WORDS: 
                        if len(M_INPUT)==self.word_length  :
                            INPUTS.append(M_INPUT)
                            if M_INPUT.lower()== ANSWER :
                                FIN = True
                            else :
                                FIN = False
                            M_INPUT=""
                            toSave=True
                if self.clavierRow3[i].txt=="del":
                    if len(M_INPUT)>0 :
                        M_INPUT=M_INPUT[:len(M_INPUT)-1]
        
        
        return [M_INPUT,INPUTS,FIN,toSave,ANSWER]

    def coloration(self,input,VERT,JAUNE,color):
                
                for k in range(len(self.clavierRow1)):
                    if self.clavierRow1[k].txt ==input:
                        if self.clavierRow1[k].bodyColor!=JAUNE:
                            if self.clavierRow1[k].bodyColor!=VERT :
                            
                                self.clavierRow1[k].bodyColor=color
                        else:
                            if color == VERT:
                                self.clavierRow1[k].bodyColor=color

                        # clavierRow1[k].render(SCREEN)

                for k in range(len(self.clavierRow2)):
                    if self.clavierRow2[k].txt ==input:
                        if self.clavierRow2[k].bodyColor!=JAUNE:
                            if self.clavierRow2[k].bodyColor!=VERT :
                                self.clavierRow2[k].bodyColor=color
                        # clavierRow2[k].render(SCREEN)
                        else:
                            if color == VERT:
                                self.clavierRow2[k].bodyColor=color

                for k in range(len(self.clavierRow3)):
                    if self.clavierRow3[k].txt ==input:
                        if self.clavierRow3[k].bodyColor!=JAUNE:
                            if self.clavierRow3[k].bodyColor!=VERT :
                                self.clavierRow3[k].bodyColor=color
                        # clavierRow3[k].render(SCREEN)
                        else:
                            if color == VERT:
                                self.clavierRow3[k].bodyColor=color
