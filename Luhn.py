import requests
import json
import os
from random import randint





class Luhn :
    def __init__(self):
        self.file = 'cards.txt'
        self.choice = '1'
        self.check = '[1] Check card details \r\n'
        self.search = '[2] Generate bin cards valid \r\n'
        self.choice = 0
        self.file = None
        self.type = None

        
        
    

    @classmethod
    def controller(self):
        self.welcome()

        while True:
            self.printTools()
            self.askChoice()
            play = True
            if self.choice != 0 :
                if self.choice == '2' :
                    cardnumber = self.generate(16)
                    self.choice = 0
                if self.choice == '1' : 
                    self.choice = 0


                        

    @classmethod
    def welcome(self):
        #os.system("figlet -f banner 'Bin app Johndoe Chivas' \r\n")
        os.system("figlet 'Bin' -f small \r\n")
        os.system("figlet 'App' -f small \r\n")
        os.system("figlet 'Programmed' -f small \r\n")
        os.system("figlet 'By  ' -f small \r\n")
        os.system("figlet 'JohnDoe' -f small \r\n")
        print('\r\n')
    
    @classmethod
    def printTools(self):
        print(self.check)
        print(self.search)

    @classmethod
    def askChoice(self):
        choix = ''
        while choix == '':
            choix = input('[-] Choose what you want do ? : ')
        
        self.choice = choix
        return self.choice

    

    @classmethod
    def luhn(self,digits):
        transformLuhn = []
        digitsReverse = digits[::-1]
        sumOrig = 0
        sumLuhn = 0
        rankPlace = 0

        print('Array original : ' + str(digits))
        print('Array reverse : '+str(digitsReverse))
        

        # doubler et faire la sum des chiffres si n * 2 > 10
        
        for double in digitsReverse :
            if rankPlace % 2 != 0 :
                double = int(double) * 2
                if ( double > 2):
                    sumstringify = 0
                    stringify = str(double)
                    for i in stringify :
                        sumstringify = sumstringify + int(i)
                        double = sumstringify
                
                transformLuhn.append(double)
            rankPlace = rankPlace + 1
        ###########################################

        
        # faire la somme original dans le sens de lecture de la fin
        for digit in digitsReverse :
            if (rankPlace % 2) == 0 :
                sumOrig = sumOrig + int(digit)    
            rankPlace = rankPlace + 1
        

        for nb in transformLuhn : 
            sumLuhn = sumLuhn + int(nb)
        total = sumOrig + sumLuhn
        print('Sum array original : '+str(sumOrig))
        print('Sum array luhn : '+str(sumLuhn))
        print('Sum complete : '+str(total))
        

        ###########################################


        # verifier que le total est modulo 10

        if total % 10 == 0 :
            return True
        else :
            return False
    
    @classmethod
    def random_with_N_digits(self,digits):
        return randint(10**(int(digits)-1), (10**int(digits)-1))

    @classmethod # generate une CB qui respecte la formule de Luhn
    def randomBin(self,digits):
        genNumber = 1
        random = 0
        randomBin = True
        while randomBin :
            print('Try #'+str(genNumber))
            random = self.random_with_N_digits(digits)
            valid = self.luhn(str(random))
            if valid == True :
                print('Luhn\'s algorithm respected for : '+str(random))
                randomBin = False
            genNumber = genNumber + 1
            print('\r\n')
        return random
        
        

    @classmethod
    def verifyLuhn(self,bin):
        valid = self.luhn(bin)
        if valid == True: 
            print('carte valide')
            return valid
        else :
            print('carte non valide')
            return False
    
    @classmethod
    def verifyCard(self,bin):
        check = True
        reponse = requests.post("https://lookup.binlist.net/"+str(bin))
        try : 
            text = ''
            jsonData = json.loads(reponse.text)
            try: 
                if jsonData['scheme'] is not None : 
                    print('Scheme : '+jsonData['scheme'])
                    text = text+'Scheme : '+jsonData['scheme']+'\r\n'
                    self.scheme = jsonData['scheme']
            except KeyError :
                pass
            except TypeError:
                pass
            try:         
                if jsonData['type'] is not None : 
                    print('Type : '+jsonData['type'])
                    text = text+'Type : '+jsonData['type']+"\r\n"
                    self.type = jsonData['type']
            except KeyError :
                pass
            except TypeError:
                pass
            try : 
                if jsonData['country']['name'] is not None : 
                     print('Pays : '+jsonData['country']['name'])
                     text = text+'Pays : '+jsonData['country']['name']+"\r\n"
                     self.country = jsonData['country']['name']

            except KeyError :
                pass
            except TypeError:
                pass
            try : 
                if jsonData['country']['currency'] is not None : 
                    print('Currency : '+jsonData['country']['currency'])
                    text = text + 'Currency : '+jsonData['country']['currency']+"\r\n"
                    self.currency = jsonData['country']['currency']
            
            except KeyError :
                pass
            except TypeError:
                pass
            try :     
                if jsonData['brand'] is not None : 
                    print('Marque : '+jsonData['brand'])
                    text = text + 'Marque : '+jsonData['brand']+"\r\n"
                    self.marque = jsonData['brand']
            except KeyError :
                pass
            except TypeError:
                pass
            try : 
                if jsonData['bank']['name'] is not None : 
                    print('Bank : '+jsonData['bank']['name'])
                    text = text + 'Bank : '+jsonData['bank']['name']+"\r\n"
                    self.bank = jsonData['bank']['name']
            except KeyError :
                pass
            except TypeError:
                pass
            try : 
                if jsonData['bank']['url'] is not None : 
                    print('Website : '+jsonData['bank']['url'])
                    text = text + 'Website : '+jsonData['bank']['url']+"\r\n"
                    self.website = jsonData['bank']['url']
            except KeyError :
                pass
            except TypeError:
                pass
            

        #except KeyError :
            #pass
        #except TypeError:
            #pass
                
        except json.decoder.JSONDecodeError:
            check = False
        
        print('\r\n')
        if check == True :
            text = text+ 'BIN : '+str(bin)+"\r\n\n"
            self.writeData(text)
        return check


    @classmethod
    def generate(self,digits):
        while True:
            gen = self.randomBin(digits)
            print('Checking credit card '+str(gen)+' exists \r\n')
            os.system("sleep 2s")
            validCard = self.verifyCard(gen)
            if validCard == True : 
                #print('Credit card find : '+str(gen)+'\r\n')
                os.system("sleep 2s")
                self.bin = gen
                return gen
            else: 
                print('No credit card find')
                os.system("sleep 2s")
                
        
    @classmethod
    def writeData(self,key):
        """
        write keyboard data into file log
        """
       
        fileLog = open('cards.txt','a')
        fileLog.write(key)
        
        fileLog.close()
        
"""
test = Luhn(0)
test.controller()
"""
