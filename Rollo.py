from NumericStringParser import NumericStringParser
from random import randrange
class Rollo:
    nsp = None
    wordsList = []
    parsed = ""
    result = ""
    def __init__(self):
        self.nsp = NumericStringParser()

    def parse(self,toParse):
        toParse = self.addSpaces(toParse).upper()
        self.wordsList = self.separateWords(toParse)
        self.parsed = " ".join(self.wordsList)
        self.result = " ".join(self.rollDices())
        self.result += " = "+str(self.nsp.eval(self.result))
        #print("words list: "+str(self.wordsList))
        print("parsed: "+self.parsed)
        print("result: "+self.result)

    def addSpaces(self,string):
        #insert spaces in-between a char and a "math char"
        char_list = ["+","-","/","*","(",")","[","]","{","}"]
        for char in char_list:
            index = 0
            #print("start with "+char)
            while index != -1:
                index = string.find(char,index)
                if index>=0:
                    flag = True if index-1>0 and string[index-1].isspace() else False
                    string = string[:index]+("" if flag else " ")+string[index]+("" if index+1<len(string) and string[index+1].isspace() else " ")+string[index+1:]
                    # I use bool flag because is the same check
                   # print(string)
                   # print('flag is '+str(flag)+ " so"+ (" there si already a space" if flag else "there is no space"))
                    index+= 1 if flag else 2
        return string

    def separateWords(self,string):
        return string.split()
    
    def rollDices(self):
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

    def roll(self,diceString):
        numberList = diceString.split("D")
        times = int(numberList[0])
        faces = int(numberList[1])
        rolledDicesList = []
        for i in range(times):
            rolledDicesList.append(randrange(faces)+1)
        return " + ".join( [str(num) for num in rolledDicesList] ) 

