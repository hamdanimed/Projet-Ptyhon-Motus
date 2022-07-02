import speech_recognition as sr
from colors import getLangue



def recognize_speech_from_mic(recognizer,microphone,queue):
    language=getLangue()
    if language == "fr":
        voicelanguage=language+"-FR"
    if language == "en":
        voicelanguage=language+"-US"


    if not isinstance(recognizer,sr.Recognizer):
        raise TypeError("recognizer must be instance of Recognizer")
    
    if not isinstance(microphone,sr.Microphone):
        raise TypeError("microphone must be instance of Microphone")

    response={
        "success":True,            #success contient True ou False selon la demande d'API 
        "error":None,              #error contient None si tout se passe bien sinon elle cotient l'erreur produite qui depend de l'echec d'API ou la transcription na pas reussie
        "transcription":None       #transcription soit rien si une erreur s'est produite ou le texte transcrit si l'operation a bien reussie
    }
    with microphone as source:
        
        # recognizer.adjust_for_ambient_noise(source,duration=0.5)
        recognizer.energy_threshold=3000
       
        audio_data=recognizer.listen(source)
    
    
    try:
        
        response["transcription"]=recognizer.recognize_google(audio_data,language=voicelanguage)
        
    except sr.RequestError:
        response["success"]=False
        response["error"]="API unreached"
    except sr.UnknownValueError:
        response["success"]=False
        response["error"]="failed to recognize audio"
    
    queue.put(response)  #on insere la reponse dans la queue clavier.inputMicQueue








    
