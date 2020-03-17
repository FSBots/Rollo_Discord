from NumericStringParser import NumericStringParser
from random import randrange
class Rollo:
    nsp = None
    char_list = ["+","-","/","*","(",")","[","]","{","}"]
    advantage_keyword_list = ["VANTAGGIO","ADVANTAGE"]
    disadvantage_keyword_list = ["SVANTAGGIO","DISADVANTAGE"]
    keyword_list = ["TIRO","TIRA","ROLL"]
    wordsListBackup = []
    wordsList = []
    parsed = ""
    result = ""
    result2 = ""
    isACorrectCommand = False
    isACorrectExpression = False
    advantage = 0 # 0: none 1:advantage -1: disadvantage
    def __init__(self):
        self.nsp = NumericStringParser()

    def parse(self,toParse):
        toParse = self.addSpaces(toParse).upper()
        #print("ToParse => "+str(toParse))
        self.wordsList = self.separateWords(toParse)
        self.checkCommand()
        self.checkAdvantageDisadvantage()
        if self.isACorrectCommand: # i found a "roll" keyword
            self.parsed = " ".join(self.wordsList)
            if self.advantage!=0: #I backup words list because it will be modified by rollDices
                self.wordsListBackup = self.wordsList.copy()
            self.result = " ".join(self.rollDices())
            self.checkExpression()
            if self.advantage!=0: #Launch a second time becaus i found advantage or disadvantage keyword
                self.wordsList = self.wordsListBackup
                self.result2 = " ".join(self.rollDices())
            if self.isACorrectExpression:
                try:
                    self.result += " = "+str(self.nsp.eval(self.result))
                    if self.advantage != 0:
                        self.result2 += " = "+str(self.nsp.eval(self.result2))
                        self.result += "\n" +self.result2
                    #print("words list: "+str(self.wordsList))
                except:
                    self.result = "ERROR INCORRECT MATH EXPRESSION"
                print("parsed: "+self.parsed)
                print("result: "+self.result)   
            else:
                self.result = ""
    def checkAdvantageDisadvantage(self):#advantage disadvantage must be put as last keyword on the command line
        if self.wordsList[-1] in self.advantage_keyword_list:
            self.advantage = 1
            del self.wordsList[-1]
        elif  self.wordsList[-1] in self.disadvantage_keyword_list:
            self.advantage = -1
            del self.wordsList[-1]
        pass

    def getParsedString(self):
        return self.parsed
    def getResultString(self):
        return self.result

    def addSpaces(self,string):
        #insert spaces in-between dices and math simbols
        for char in self.char_list:
            index = 0
            #print("start with "+char)
            while index != -1:
                index = string.find(char,index)
                if index>=0:
                    flag = True if index-1>0 and string[index-1].isspace() else False
                    string = string[:index]+("" if flag else " ")+string[index]+("" if index+1<len(string) and string[index+1].isspace() else " ")+string[index+1:]
                    # I recycle bool flag because is the same check
                   # print(string)
                   # print('flag is '+str(flag)+ " so"+ (" there si already a space" if flag else "there is no space"))
                    index+= 1 if flag else 2
        return string

    def separateWords(self,string):
        return string.split()

    def checkCommand(self): # first word is TIRO or ROLL?
        if self.wordsList[0] in self.keyword_list:
            self.isACorrectCommand = True
            del self.wordsList[0]
        else:
            self.isACorrectCommand = False
        pass

    def checkExpression(self): #maybe not well optimized, but it works
        list = self.wordsList.copy()
        i = 0
        words = []
        #print("initial list => "+str(list))
        for i in range(len(list)):
            #print("index: "+str(i))
            words+=(self.separateWords(list[i]))
            # i have to this because 3D5 result as one string like '2 + 1 + 4', but it must be '2','+','1','+','4'
            #print("words list found => "+str(words))
        list = words
        #print("list => "+str(list))

        validElementChecked = 0 #At the end its value must be as big as len(list) if no the command line is incorrect
        for i in range(len(list)):
            #print('esamino => '+list[i])
            if list[i] in self.char_list:
                #print("È nei caratteri speciali")
                validElementChecked+=1
            else:
                try:
                    int(list[i])
                    #print("È un numero")
                    validElementChecked+=1
                except:
                    #print("found a no-number")
                    break
        #print("Da eliminare => "+str(validElementChecked))
        #print(list)

        self.isACorrectExpression = True if len(list)==validElementChecked else False
        #print("L'espressione è = "+str(self.isACorrectExpression)+" perché len = "+str(len(list))+" e ho trovato "+str(validElementChecked)+" elementi validi")
        pass


    def rollDices(self):# For every dice found ( find dice ) run roll it and replace the dice string with the roll result string
        index = 0
        index = self.findDice(self.wordsList)
        while(index!=-1):
            self.wordsList[index] = str(self.roll(self.wordsList[index]))
            index = self.findDice(self.wordsList)
        
        return self.wordsList

    def findDice(self,list):
        for x in range(len(list)):
            if list[x].find("D") != -1:
                return x
        return -1

    def roll(self,diceString): # roll a dice
        numberList = diceString.split("D")
        #print("numeri "+str(numberList))
        try:
            if numberList[0]!="": #example D20 means 1D20
                times = int(numberList[0])
                faces = int(numberList[1])
            else:
                times = 1
                faces = int(numberList[1])
        except:
            return ""
        rolledDicesList = []
        for i in range(times):
            rolledDicesList.append(randrange(faces)+1)
        return " + ".join( [str(num) for num in rolledDicesList] ) 

