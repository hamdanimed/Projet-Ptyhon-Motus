import json
#function: empties the attempts from the json
def DelAttempts(sespth,d):
    f2 = open(sespth,'w')
    for i in range(0,6):
        d["attempt"+str(i)]=""
    json.dump(d,f2)
    f2.close()

#function: save session in json file (only happens when you quit, otherwise everything stays in python until you exit)
def SaveSession(sespth,d,ans,sc,inp,wl):
    f2 = open(sespth,'w')
    d['guess'] = ans
    d['score'] = sc
    d["lengthsix"] = (wl==6)
    for i in range(len(inp)):
        d["attempt"+str(i)] = inp[i]
    json.dump(d,f2)
    f2.close()


#session functions are now with arguments, they can be used in all interfaces


