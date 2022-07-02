# LIKING CODE

from main_menu import main_menu
Queue=[main_menu]

def addToList(interfaceFct):
    Queue.append(interfaceFct)

def removeFromList():
    Queue.pop()

def interfaceDecider():
    Queue[-1]()
