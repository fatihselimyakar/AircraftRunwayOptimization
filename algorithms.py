import re
import string
import math
from random import seed
from random import random
from random import randint
from datetime import datetime
import time

E = 2.71828

# Holds aircraft set properties
class AircraftsSetSample:
    # data
    def __init__(self):
        self.nOfRunways = 0
        self.nOfAircrafts = 0
        self.readyTimes = []
        self.dueTimes = []
        self.aircraftTypes = []
        self.operationTypes = []
        self.weights = []
        self.startTimes = []
        self.minimumSeperationTimes = []

# Holds aircraf set property array and initializes by reading txt file
class AircraftsSet:
    def __init__(self):
        self.set=[]

    # reads the data in txt file and assigns the self.set's variables
    def readDataSet(self,inputString):
        # Using readlines() 
        inputFile = open(inputString, 'r') 
        Lines = inputFile.readlines()
        rowNum=0
        rowLimit=7
        setSize=0
        for line in Lines:
            if line[0]!='%' and line[0]!=' ' and line[0]!= '\n':
                lineItems=re.split('\W+',line)
                tokenNum=0
                for lineItem in lineItems:
                    #print(lineItem,end=" ")
                    if lineItem=='':
                        break
                    if rowNum==0 and tokenNum==0:
                        self.set.append(AircraftsSetSample())
                        self.set[setSize].nOfRunways=int(lineItem)
                    elif rowNum==1 and tokenNum==0:
                        self.set[setSize].nOfAircrafts=int(lineItem)
                        rowLimit=rowLimit+(self.set[setSize].nOfAircrafts)
                    elif rowNum==2:
                        self.set[setSize].readyTimes.append(float(lineItem)/60)
                    elif rowNum==3:
                        self.set[setSize].dueTimes.append(float(lineItem)/60)
                    elif rowNum==4:
                        self.set[setSize].aircraftTypes.append(int(lineItem))
                    elif rowNum==5:
                        self.set[setSize].operationTypes.append(int(lineItem))
                    elif rowNum==6:
                        self.set[setSize].weights.append(int(lineItem))
                    elif rowNum>=7:
                        if(rowNum==7 and tokenNum==0):
                            for i in range(0,self.set[setSize].nOfAircrafts):
                                lst=[0]*self.set[setSize].nOfAircrafts
                                self.set[setSize].minimumSeperationTimes.append(lst)
                        self.set[setSize].minimumSeperationTimes[rowNum-7][tokenNum]=float(lineItem)/60
                    tokenNum+=1
                #print()
                rowNum+=1
                if(rowNum==rowLimit):
                    rowNum=0
                    rowLimit=7
                    setSize+=1
            if setSize==60:
                break
        inputFile.close()

    # prints the properties of given indexed set
    def printSet(self,index):
        aircraftSize=self.set[index].nOfAircrafts
        print("Runway numb:")
        print(self.set[index].nOfRunways)
        print("Aircraft numb:")
        print(self.set[index].nOfAircrafts)

        print("Ready times:")
        for i in range(0,aircraftSize):
            print(self.set[index].readyTimes[i]*60,end=" ")
        print("")

        print("Due times:")
        for i in range(0,aircraftSize):
            print(self.set[index].dueTimes[i]*60,end=" ")
        print("")

        print("Aircraft types:")
        for i in range(0,aircraftSize):
            print(self.set[index].aircraftTypes[i],end=" ")
        print("")

        print("Operation types:")
        for i in range(0,aircraftSize):
            print(self.set[index].operationTypes[i],end=" ")
        print("")

        print("Weights:")
        for i in range(0,aircraftSize):
            print(self.set[index].weights[i],end=" ")
        print("")

        print("Seperation times:")
        for i in range(0,aircraftSize):
            for j in range(0,aircraftSize):
                print(self.set[index].minimumSeperationTimes[i][j]*60,end=" ")
            print("")

# Parent class that provides basic same methods
class Algorithm:
    def __init__(self):
        self.set=AircraftsSetSample()
    def setAircraftsSet(self,setSample):
        self.set=setSample

    def findMinIndex(self,array):
        i=0
        index=0
        minimum=float('inf')
        for i in range(0,len(array)):
            if(array[i]<minimum):
                minimum=array[i]
                index=i
        return index

    def piFormula(self,j,t,k):
        #return float(self.set.weights[j])*math.exp(float(-max(self.set.readyTimes[j]-t,0)))*math.exp(float(-self.set.minimumSeperationTimes[k][j]))*math.exp(float(-max((self.set.readyTimes[j]+1/3)-t,0)))*math.exp(float(-max(self.set.dueTimes[j]-t,0)))
        return math.exp(float(-max(self.set.readyTimes[j]-t,0)))*math.exp(float(-self.set.minimumSeperationTimes[k][j]))*math.exp(float(-max((self.set.readyTimes[j]+1/3)-t,0)))*math.exp(float(-max(self.set.dueTimes[j]-t,0)))

    def fpiFormula(self,j,t,k):
        #return float(self.set.weights[j])*(1/max(self.set.readyTimes[j]-t,1))*(1/max(self.set.readyTimes[j]+1/3-t,1))*(1/max(self.set.dueTimes[j]-t,1))*(1/self.set.minimumSeperationTimes[k][j])
        return (1/max(self.set.readyTimes[j]-t,1))*(1/max(self.set.readyTimes[j]+1/3-t,1))*(1/max(self.set.dueTimes[j]-t,1))*(1/self.set.minimumSeperationTimes[k][j])
    
    def greedyAlgorithm(self,formulaMethod):
        aircraftSize=self.set.nOfAircrafts
        sortedAircrafts=[0]*aircraftSize
        results=[0]*aircraftSize
        endTime=0

        for i in range(0,aircraftSize):
            self.set.startTimes.append(0)
        
        J=[0]*aircraftSize
        for i in range(0,aircraftSize):
            J[i]=i

        minReadyIndex=self.findMinIndex(self.set.readyTimes)
        lastAircraftOperated=minReadyIndex
        self.set.startTimes[minReadyIndex]=self.set.readyTimes[minReadyIndex]
        J[lastAircraftOperated]=-1
        sortedAircrafts[0]=lastAircraftOperated
        results[lastAircraftOperated]=self.set.startTimes[minReadyIndex]*60
        for index in range(1,aircraftSize):
            maximum=float('-inf')
            formulaSolution=0
            startTimeForAircraftI=0
            chosenAircraft=0
            chosenAircraftStartTime=0
            for i in range(0,aircraftSize):
                if(J[i]!=-1):
                    startTimeForAircraftI=max(self.set.readyTimes[i],self.set.startTimes[lastAircraftOperated]+self.set.minimumSeperationTimes[lastAircraftOperated][i])
                    formulaSolution=formulaMethod(i,startTimeForAircraftI,lastAircraftOperated)
                    if(formulaSolution>maximum):
                        maximum=formulaSolution
                        chosenAircraft=i
                        chosenAircraftStartTime=startTimeForAircraftI
            J[chosenAircraft]=-1
            self.set.startTimes[chosenAircraft]=chosenAircraftStartTime
            lastAircraftOperated=chosenAircraft
            results[chosenAircraft]=chosenAircraftStartTime*60
            if(results[chosenAircraft]>endTime):
                endTime=results[chosenAircraft]
            sortedAircrafts[index]=chosenAircraft

        return endTime,results,sortedAircrafts

    def findStartTime(self,solutionArray,willPrint):
        aircraftSize=self.set.nOfAircrafts
        startTimes=[0]*aircraftSize
        startTimes[0]=self.set.readyTimes[solutionArray[0]]
        resultStartTime=0
        deadlineExceed=0
        for i in range(1,aircraftSize):
            startTimes[i]=max(self.set.readyTimes[solutionArray[i]],startTimes[i-1]+self.set.minimumSeperationTimes[solutionArray[i-1]][solutionArray[i]])
            #if(self.set.dueTimes[solutionArray[i]]<startTimes[i]):
            #    deadlineExceed+=1
            if(willPrint):
                print("seperation ",solutionArray[i-1],solutionArray[i],self.set.minimumSeperationTimes[solutionArray[-1]][solutionArray[i]]*60)
            if(resultStartTime<startTimes[i]):
                resultStartTime=startTimes[i]
        if(willPrint):
            for i in range(0,aircraftSize):
                print("Aircraft ",solutionArray[i]," Start time ",startTimes[i]*60)

        #resTime=resultStartTime*60+deadlineExceed*500
        return resultStartTime*60,startTimes


    def pathExchangeNeighbourhood(self,solutionArray):
        size=len(solutionArray)
        startIndex=int(size/2)
        pathSize=randint(0,startIndex-1)

        for i in range(0,pathSize):
            solutionArray[i],solutionArray[startIndex+i]=solutionArray[startIndex+i],solutionArray[i]


    def itemExchangeNeighbourhood(self,solutionArray):
        size=len(solutionArray)
        firstIndex=randint(0,size-1)
        secondIndex=randint(0,size-1)
        while(firstIndex==secondIndex):
            secondIndex=randint(0,size-1)

        solutionArray[firstIndex],solutionArray[secondIndex]=solutionArray[secondIndex],solutionArray[firstIndex]

    def neighbourhoodSearch(self,solutionArray,neighbourhoodType):
        neighbourhoodType(solutionArray)



class ERT(Algorithm):

    def ERT(self):
        aircraftSize=self.set.nOfAircrafts
        sortedAircrafts=[0]*aircraftSize
        results=[0]*aircraftSize
        endTime=0

        for i in range(0,aircraftSize):
            self.set.startTimes.append(0)
        
        J=[0]*aircraftSize
        for i in range(0,aircraftSize):
            J[i]=i

        minReadyIndex=self.findMinIndex(self.set.readyTimes)
        lastAircraftOperated=minReadyIndex
        self.set.startTimes[minReadyIndex]=self.set.readyTimes[minReadyIndex]
        J[lastAircraftOperated]=-1
        sortedAircrafts[0]=lastAircraftOperated
        results[lastAircraftOperated]=self.set.startTimes[minReadyIndex]*60
        for index in range(1,aircraftSize):
            minimum=float('inf')
            startTimeForAircraftI=0
            chosenAircraft=0
            chosenAircraftStartTime=0
            for i in range(0,aircraftSize):
                if(J[i]!=-1):
                    startTimeForAircraftI=max(self.set.readyTimes[i],self.set.startTimes[lastAircraftOperated]+self.set.minimumSeperationTimes[lastAircraftOperated][i])
                    if(self.set.readyTimes[i]<minimum):
                        minimum=self.set.readyTimes[i]
                        chosenAircraft=i
                        chosenAircraftStartTime=startTimeForAircraftI
            J[chosenAircraft]=-1
            self.set.startTimes[chosenAircraft]=chosenAircraftStartTime
            lastAircraftOperated=chosenAircraft
            results[chosenAircraft]=chosenAircraftStartTime*60
            if(results[chosenAircraft]>endTime):
                endTime=results[chosenAircraft]
            sortedAircrafts[index]=chosenAircraft
        
        return endTime,results,sortedAircrafts

class AATCSR(Algorithm):
    
    def AATCSR(self):
        return self.greedyAlgorithm(self.piFormula)

class FPI(Algorithm):
    
    def FPI(self):
        return self.greedyAlgorithm(self.fpiFormula)

class SA(Algorithm):

    def genericSA(self,initialSolutionArray,innerLoop,temperatureCooling,reheatLoop,array):
        aircraftSize=self.set.nOfAircrafts
        initialSolution=initialSolutionArray[2]
        fTeta=initialSolutionArray[0]
        reheatTemperature=initialSolutionArray[0]
        bestTeta=float('inf')
        bestSolution=[0]*aircraftSize
        for reheatCounter in range(reheatLoop):
            i=0
            c=0
            temperature=reheatTemperature
            while(temperature>0.002):
                i=0
                while(i<innerLoop):
                    newSolution=[0]*aircraftSize
                    newSolution=initialSolution.copy()
                    self.neighbourhoodSearch(newSolution,self.itemExchangeNeighbourhood)
                    fNewTeta=self.findStartTime(newSolution,0)[0]
                    if((fNewTeta-fTeta<=0) or (random()<=math.exp(-((fNewTeta-fTeta)/temperature)))):
                        fTeta=fNewTeta
                        initialSolution=newSolution.copy()
                    if(fTeta<bestTeta):
                        bestTeta=fTeta
                        bestSolution=initialSolution.copy()
                    i+=1
                temperature*=temperatureCooling
                #print(str(int(bestTeta))+','+str(int(fTeta)))
                if(c%100==0):
                    array.append(int(bestTeta))
                c+=1
            array.append(int(bestTeta))
            reheatTemperature*=0.8
        return bestTeta,bestSolution

    def SAaatcsr(self,innerLoop,temperatureCooling,reheatLoop,array):
        aatcsr=AATCSR()
        aatcsr.setAircraftsSet(self.set)
        return self.genericSA(aatcsr.AATCSR(),innerLoop,temperatureCooling,reheatLoop,array)

    def SAert(self,innerLoop,temperatureCooling,reheatLoop,array):
        ert=ERT()
        ert.setAircraftsSet(self.set)
        return self.genericSA(ert.ERT(),innerLoop,temperatureCooling,reheatLoop,array)

    def SAfpi(self,innerLoop,temperatureCooling,reheatLoop,array):
        fpi=FPI()
        fpi.setAircraftsSet(self.set)
        return self.genericSA(fpi.FPI(),innerLoop,temperatureCooling,reheatLoop,array)

class metaRaps(Algorithm):

    def metaRapsLoop(self,formulaMethod,changeProb):
        aircraftSize=self.set.nOfAircrafts
        sortedAircrafts=[0]*aircraftSize
        results=[0]*aircraftSize
        endTime=0

        for i in range(0,aircraftSize):
            self.set.startTimes.append(0)
        
        J=[0]*aircraftSize
        for i in range(0,aircraftSize):
            J[i]=i

        minReadyIndex=self.findMinIndex(self.set.readyTimes)
        lastAircraftOperated=minReadyIndex
        self.set.startTimes[minReadyIndex]=self.set.readyTimes[minReadyIndex]
        J[lastAircraftOperated]=-1
        sortedAircrafts[0]=lastAircraftOperated
        results[lastAircraftOperated]=self.set.startTimes[minReadyIndex]*60

        for index in range(1,aircraftSize):
            maximum=float('-inf')
            formulaSolution=0
            startTimeForAircraftI=0
            chosenAircraft=0
            chosenAircraftStartTime=0
            s=0
            for i in range(0,aircraftSize):
                if(J[i]!=-1):
                    startTimeForAircraftI=max(self.set.readyTimes[i],self.set.startTimes[lastAircraftOperated]+self.set.minimumSeperationTimes[lastAircraftOperated][i])
                    formulaSolution=formulaMethod(i,startTimeForAircraftI,lastAircraftOperated)
                    if(formulaSolution>maximum):
                        maximum=formulaSolution
                        chosenAircraft=i
                        chosenAircraftStartTime=startTimeForAircraftI
            p=random()
            if(p<=changeProb):
                s=chosenAircraft
            else:
                ct=0
                j=randint(0,aircraftSize-1)
                startTimeForAircraftJ=max(self.set.readyTimes[j],self.set.startTimes[lastAircraftOperated]+self.set.minimumSeperationTimes[lastAircraftOperated][j])
                localFormulaSolution=formulaMethod(j,startTimeForAircraftJ,lastAircraftOperated)
                while(J[j]==-1 or (localFormulaSolution<(formulaSolution*0.25))):
                    j=randint(0,aircraftSize-1)
                    startTimeForAircraftJ=max(self.set.readyTimes[j],self.set.startTimes[lastAircraftOperated]+self.set.minimumSeperationTimes[lastAircraftOperated][j])
                    maximum=localFormulaSolution
                    ct+=1
                    if(ct==1000):
                        j=chosenAircraft
                        startTimeForAircraftJ=chosenAircraftStartTime
                        maximum=formulaSolution
                        break
                    localFormulaSolution=formulaMethod(j,startTimeForAircraftJ,lastAircraftOperated)
                s=j
                chosenAircraftStartTime=startTimeForAircraftJ
                formulaSolution=localFormulaSolution
            chosenAircraft=s
            
            J[chosenAircraft]=-1
            self.set.startTimes[chosenAircraft]=chosenAircraftStartTime
            lastAircraftOperated=chosenAircraft

            results[chosenAircraft]=chosenAircraftStartTime*60

            if(results[chosenAircraft]>endTime):
                endTime=results[chosenAircraft]
            sortedAircrafts[index]=chosenAircraft
        return endTime,results,sortedAircrafts

    def metaRapsErtLoop(self,changeProb):
        aircraftSize=self.set.nOfAircrafts
        sortedAircrafts=[0]*aircraftSize
        results=[0]*aircraftSize
        endTime=0

        for i in range(0,aircraftSize):
            self.set.startTimes.append(0)
        
        J=[0]*aircraftSize
        for i in range(0,aircraftSize):
            J[i]=i

        minReadyIndex=self.findMinIndex(self.set.readyTimes)
        lastAircraftOperated=minReadyIndex
        self.set.startTimes[minReadyIndex]=self.set.readyTimes[minReadyIndex]
        J[lastAircraftOperated]=-1
        sortedAircrafts[0]=lastAircraftOperated
        results[lastAircraftOperated]=self.set.startTimes[minReadyIndex]*60

        for index in range(1,aircraftSize):
            minimum=float('inf')
            formulaSolution=0
            startTimeForAircraftI=0
            chosenAircraft=0
            chosenAircraftStartTime=0
            s=0
            for i in range(0,aircraftSize):
                if(J[i]!=-1):
                    startTimeForAircraftI=max(self.set.readyTimes[i],self.set.startTimes[lastAircraftOperated]+self.set.minimumSeperationTimes[lastAircraftOperated][i])
                    if(formulaSolution<minimum):
                        minimum=formulaSolution
                        chosenAircraft=i
                        chosenAircraftStartTime=startTimeForAircraftI
            p=random()
            if(p<=changeProb):
                s=chosenAircraft
            else:
                ct=0
                j=randint(0,aircraftSize-1)
                startTimeForAircraftJ=max(self.set.readyTimes[j],self.set.startTimes[lastAircraftOperated]+self.set.minimumSeperationTimes[lastAircraftOperated][j])
                while(J[j]==-1 or (startTimeForAircraftJ<(chosenAircraftStartTime*0.25))):
                    j=randint(0,aircraftSize-1)
                    startTimeForAircraftJ=max(self.set.readyTimes[j],self.set.startTimes[lastAircraftOperated]+self.set.minimumSeperationTimes[lastAircraftOperated][j])
                    ct+=1
                    if(ct==1000):
                        j=chosenAircraft
                        startTimeForAircraftJ=chosenAircraftStartTime
                        break
                s=j
                chosenAircraftStartTime=startTimeForAircraftJ
            chosenAircraft=s
            
            J[chosenAircraft]=-1
            self.set.startTimes[chosenAircraft]=chosenAircraftStartTime
            lastAircraftOperated=chosenAircraft

            results[chosenAircraft]=chosenAircraftStartTime*60

            if(results[chosenAircraft]>endTime):
                endTime=results[chosenAircraft]
            sortedAircrafts[index]=chosenAircraft
        return endTime,results,sortedAircrafts

    def metaRaps(self,metaLoop,formulaMethod,changeProb,loopSize,array):
        aircraftSize=self.set.nOfAircrafts
        endTime=0
        solutionTime=0
        bestTime=float('inf')
        worstTime=0
        solutionArray=[0]*aircraftSize
        bestSolutionArray=[0]*aircraftSize

        for i in range(0,loopSize):
            result=metaLoop(formulaMethod,changeProb)
            solutionArray=result[2]
            endTime=result[0]
            solutionTime=endTime
            if(worstTime<solutionTime):
                worstTime=solutionTime
            if(bestTime>solutionTime):
                bestTime=solutionTime
                bestSolutionArray=solutionArray.copy()
            if(solutionTime<=(bestTime+((worstTime-bestTime)*0.9))):
                self.neighbourhoodSearch(solutionArray,self.pathExchangeNeighbourhood)
                newTime=self.findStartTime(solutionArray,0)[0]
                if(newTime<=bestTime):
                    bestTime=newTime
                    bestSolutionArray=solutionArray.copy()
            if(i%500==0):
                array.append(int(bestTime))

        return bestTime,bestSolutionArray

    # Main meta raps functions
    def metaRapsAatcsr(self,changeProb,loopSize,array):
        return self.metaRaps(self.metaRapsLoop,self.piFormula,changeProb,loopSize,array)

    def metaRapsFpi(self,changeProb,loopSize,array):
        return self.metaRaps(self.metaRapsLoop,self.fpiFormula,changeProb,loopSize,array)

    def metaRapsErt(self,changeProb,loopSize,array):
        aircraftSize=self.set.nOfAircrafts
        endTime=0
        solutionTime=0
        bestTime=float('inf')
        worstTime=0
        solutionArray=[0]*aircraftSize
        bestSolutionArray=[0]*aircraftSize

        for i in range(0,loopSize):
            result=self.metaRapsErtLoop(changeProb)
            solutionArray=result[2]
            endTime=result[0]
            solutionTime=endTime
            if(worstTime<solutionTime):
                worstTime=solutionTime
            if(bestTime>solutionTime):
                bestTime=solutionTime
                bestSolutionArray=solutionArray.copy()
            if(solutionTime<=(bestTime+((worstTime-bestTime)*0.9))):
                self.neighbourhoodSearch(solutionArray,self.pathExchangeNeighbourhood)
                newTime=self.findStartTime(solutionArray,0)[0]
                if(newTime<=bestTime):
                    bestTime=newTime
                    bestSolutionArray=solutionArray.copy()
            if(i%500==0):
                array.append(int(bestTime))
        

        return bestTime,bestSolutionArray

class GA(Algorithm):
    def createRandomPopulation(self,populationSize,chromosomeLength):
        genes=[]
        for i in range(0,populationSize):
            temp=[0]*chromosomeLength
            genes.append(temp)
        
        for i in range(0,populationSize):
            for j in range(0,chromosomeLength):
                genes[i][j]=j

        for i in range(0,populationSize):
            for j in range(0,chromosomeLength):
                rand= randint(0,chromosomeLength-1)
                genes[i][rand],genes[i][j]=genes[i][j],genes[i][rand]

        #genes[0]=self.greedyAlgorithm(self.piFormula)[2]
        #genes[2]=self.greedyAlgorithm(self.fpiFormula)[2]

        return genes

    def rouletteWheelSelection(self,fitnessArray,totalFitnessValue):
        fitnessArraySize=len(fitnessArray)
        upperBound=0
        lowerBound=0
        rand=random()*totalFitnessValue

        for i in range(0,fitnessArraySize):
            if(i==0):
                upperBound=fitnessArray[0]
                lowerBound=0
            else:
                lowerBound+=fitnessArray[i-1]
                upperBound+=fitnessArray[i]
            if(rand>=lowerBound and rand<=upperBound):
                return i
        return i

    def createMatingPool(self,genes,populationSize,chromosomeLength):
        fitnessArray=[0]*populationSize
        totalFitnessValue=0
        totalUpdatedFitness=0
        matingPool=[]
        for i in range(0,populationSize):
            tempList=[0]*chromosomeLength
            matingPool.append(tempList)
        
        for i in range(0,populationSize):
            fitnessArray[i]=self.findStartTime(genes[i],0)[0]
            totalFitnessValue+=fitnessArray[i]
        
        for i in range(0,populationSize):
            fitnessArray[i]=totalFitnessValue/fitnessArray[i]
            totalUpdatedFitness+=fitnessArray[i]
        
        for i in range(0,populationSize):
            selection=self.rouletteWheelSelection(fitnessArray,totalUpdatedFitness)
            for j in range(0,chromosomeLength):
                matingPool[i][j]=genes[selection][j]

        return matingPool

    def isThereValue(self,value,lst):
        for i in range(0,len(lst)):
            if(lst[i]==value):
                return True
        return False

    def O1Process(self,parent1,parent2,isChild1):
        childList=[]
        randomIndex=randint(0,len(parent1)-1)
        randomSize=randint(0,len(parent1)-1-randomIndex)
        finishIndex=-1

        i=0
        while(i<len(parent1)):
            if(i<randomIndex):
                childList.append(-1)
            elif(i==randomIndex):
                j=randomIndex
                while(j<=randomIndex+randomSize):
                    if(isChild1):
                        childList.append(parent1[j])
                    else:
                        childList.append(parent2[j])

                    j+=1
                i=j-1
                finishIndex=j
            else:
                childList.append(-1)
            i+=1


        finishIndex%=len(parent2)
        missingValue=[]

        i=finishIndex
        counter=0
        while(counter<len(parent2)):
            if(isChild1):
                if(self.isThereValue(parent2[i],childList) == False):
                    missingValue.append(parent2[i])
            else:
                if(self.isThereValue(parent1[i],childList)== False):
                    missingValue.append(parent1[i])
            if(i==(len(parent2)-1)):
                i=-1

            i+=1
            counter+=1

        i=finishIndex
        j=0
        counter=0
        while(counter<len(childList)):
            if(childList[i]==-1):
                childList[i]=missingValue[j]
                j+=1
            if(i==(len(childList)-1)):
                i=-1

            i+=1
            counter+=1

        return childList
    
    def O1Crossover(self,population,xoverProb):
        randomNumber=0
        i=0
        while(i<len(population)):
            randomNumber=random()
            if(randomNumber<=xoverProb):
                child1=self.O1Process(population[i],population[i+1],True)
                child2=self.O1Process(population[i],population[i+1],False)
                population[i]=child1
                population[i+1]=child2
            i+=2

    def PMXProcess(self, parent1, parent2):
        size = min(len(parent1), len(parent2))
        p1, p2 = [0] * size, [0] * size

        for i in range(size):
            p1[parent1[i]] = i
            p2[parent2[i]] = i

        cxpoint1 = randint(0, size)
        cxpoint2 = randint(0, size - 1)
        if cxpoint2 >= cxpoint1:
            cxpoint2 += 1
        else:
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1

        for i in range(cxpoint1, cxpoint2):
            temp1 = parent1[i]
            temp2 = parent2[i]

            parent1[i], parent1[p1[temp2]] = temp2, temp1
            parent2[i], parent2[p2[temp1]] = temp1, temp2

            p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
            p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

        return parent1, parent2

    def PMXCrossover(self,population,xoverProb):
        randomNumber=0
        i=0
        while(i<len(population)):
            randomNumber=random()
            if(randomNumber<=xoverProb):
                self.PMXProcess(population[i],population[i+1])
                self.PMXProcess(population[i],population[i+1])
            i+=2

    def mutation(self,population):
        for i in range(0,len(population)):
            self.itemExchangeNeighbourhood(population[i])

    def findBestSolution(self,population):
        minimum=float('inf')
        startTime=0
        index=0
        for i in range(0,len(population)):
            startTime=self.findStartTime(population[i],0)[0]
            if(startTime<minimum):
                minimum=startTime
                index=i
        
        return minimum,population[index].copy()

    def printPop(self,population):
        for i in population:
            print(i)
        print()

    def survivorSelection(self,genes,matingPool):
        genesStartTime=0
        matingStartTime=0
        for i in range(0,len(genes)):
            matingStartTime=self.findStartTime(matingPool[i],0)[0]
            genesStartTime=self.findStartTime(genes[i],0)[0]
            if(matingStartTime<=genesStartTime):
                genes[i]=matingPool[i]

    def GA(self,populationSize,loopNum,array,xoverProb):
        genes=self.createRandomPopulation(populationSize,self.set.nOfAircrafts)
        
        i=0
        bestSolution=[]
        bestSolutionValue=float('inf')
        currentSolution=[]
        currentSolutionValue=0
        while(i<loopNum):
            matingPool=self.createMatingPool(genes,populationSize,self.set.nOfAircrafts)
            self.O1Crossover(matingPool,xoverProb)
            self.mutation(matingPool)

            result=self.findBestSolution(matingPool)
            currentSolution=result[1]
            currentSolutionValue=result[0]

            if(currentSolutionValue<bestSolutionValue):
                bestSolutionValue=currentSolutionValue
                bestSolution=currentSolution.copy()
            
            if(i%100==0):
                array.append(int(bestSolutionValue))

            self.survivorSelection(genes,matingPool.copy())
            i+=1
        
        return bestSolutionValue,bestSolution

    def GAWithLocalSearch(self,populationSize,loopNum,localSearchIter,array,xoverProb):
        result=self.GA(populationSize,loopNum,array,xoverProb)

        solution=result[1]
        steadySolution=result[1].copy()

        bestValue=result[0]
        bestSolution=[]

        currentSolution=[]
        for i in range(0,localSearchIter):
            solution=steadySolution.copy()
            self.itemExchangeNeighbourhood(solution)
            currentValue=self.findStartTime(solution,0)[0]
            if(bestValue>=currentValue):
                bestSolution=solution.copy()
                bestValue=currentValue

        return bestValue,bestSolution
    
def meanAndReturn(array):
    newArray=[0]*len(array[0])
    for j in range(len(array[0])):
        for i in range(len(array)):
            newArray[j]+=array[i][j]
        newArray[j]/=len(array)

    for i in range(len(newArray)):
        if(i<len(newArray)-1):
            print(newArray[i],end=",")
        else:
            print(newArray[i])

    return newArray

def gaPopulationSizeTest():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print("POPULATION SIZE CHANGE TEST")

    population_size=10
    for k in range(10):
        print("POP SIZE:",population_size,"LOOP:",50000/population_size)
        start_time = time.time()
        for j in range(20):
            array=[]
            for i in range(10):
                array.append([])
                algo=GA()
                algo.setAircraftsSet(aircraftSetObject.set[j])
                result=algo.GAWithLocalSearch(population_size,50000/population_size,1000,array[i],0.5)
            meanAndReturn(array)
        print("--- %s seconds --- for test:" % (time.time() - start_time),j)
        population_size+=10

def gaCrossoverProbTest():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print("XOVER PROB CHANGE TEST")

    xoverProb=0.2
    for k in range(8):
        print("XOVER PROB.:",xoverProb,"LOOP:",830)
        start_time = time.time()
        for j in range(20):
            array=[]
            for i in range(10):
                array.append([])
                algo=GA()
                algo.setAircraftsSet(aircraftSetObject.set[j])
                result=algo.GAWithLocalSearch(60,830,1000,array[i],xoverProb)
            meanAndReturn(array)
        print("--- %s seconds --- for test:" % (time.time() - start_time),j)
        xoverProb+=0.1

def gaCrossoverTypeTest():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print("XOVER TYPE TEST(PMX)")

    start_time = time.time()
    for j in range(20):
        array=[]
        for i in range(10):
            array.append([])
            algo=GA()
            algo.setAircraftsSet(aircraftSetObject.set[j])
            result=algo.GAWithLocalSearch(60,830,1000,array[i],0.5)
        meanAndReturn(array)
    print("--- %s seconds --- for test:" % (time.time() - start_time),j)

def gaIterationTest():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print("TEST ITERATON GA")

    start_time = time.time()
    for j in range(15,20):
        array=[]
        for i in range(10):
            array.append([])
            algo=GA()
            algo.setAircraftsSet(aircraftSetObject.set[j])
            result=algo.GAWithLocalSearch(60,5000,1000,array[i],0.8)
        meanAndReturn(array)
    print("--- %s seconds --- for test:" % (time.time() - start_time),j)

def gaTestGeneral():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print("TEST GENERAL GA")

    start_time = time.time()
    for j in range(0,60):
        array=[]
        for i in range(10):
            array.append([])
            algo=GA()
            algo.setAircraftsSet(aircraftSetObject.set[j])
            result=algo.GAWithLocalSearch(60,800,1000,array[i],0.8)
        meanAndReturn(array)
    print("--- %s seconds --- for test:" % (time.time() - start_time),j)

def saCoolingRatioTest():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print("COOLING RATIO CHANGE TEST")
    reheatArray=[int(664/70),int(664/80),int(664/80),int(664/99),int(664/123),int(664/124),int(664/159),int(664/215),int(664/299),int(664/664)]
    cooling_ratio=0.995
    for k in range(7):
        print("COOLING RATIO:",cooling_ratio,"INNER LOOP:",100)
        start_time = time.time()
        for j in range(0,20):
            array=[]
            for i in range(10):
                array.append([])
                algo=SA()
                algo.setAircraftsSet(aircraftSetObject.set[j])
                result=algo.SAaatcsr(100,cooling_ratio,reheatArray[k],array[i])
            meanAndReturn(array)
        print("--- %s seconds --- for test:" % (time.time() - start_time),j)
        cooling_ratio+=0.05
            
def saInnerLoopTest():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print("INNER LOOP CHANGE TEST")
    reheatArray=[int(1156/118),int(1156/254),int(1156/353),int(1156/472),int(1156/570),int(1156/692),int(1156/813),int(1156/928),int(1156/1048),int(1156/1156)]
    print(reheatArray)
    inner_loop=20
    for k in range(10):
        print("COOLING RATIO:",0.95,"INNER LOOP:",inner_loop)
        start_time = time.time()
        for j in range(20):
            array=[]
            for i in range(10):
                array.append([])
                algo=SA()
                algo.setAircraftsSet(aircraftSetObject.set[j])
                result=algo.SAaatcsr(inner_loop,0.95,reheatArray[k],array[i])
            meanAndReturn(array)
        print("--- %s seconds --- for test:" % (time.time() - start_time),j)
        inner_loop+=20  

def saIterationTest():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print("ITERATION TEST")
    
    start_time = time.time()
    for j in range(20):
        array=[]
        for i in range(10):
            array.append([])
            algo=SA()
            algo.setAircraftsSet(aircraftSetObject.set[j])
            result=algo.SAaatcsr(160,0.95,1,array[i])
        meanAndReturn(array)
    print("--- %s seconds --- for test:" % (time.time() - start_time),j)

def saReheatTest():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print("REHEAT TEST")
    
    
    start_time = time.time()
    for j in range(20):
        array=[]
        for i in range(10):
            array.append([])
            algo=SA()
            algo.setAircraftsSet(aircraftSetObject.set[j])
            result=algo.SAaatcsr(160,0.95,10,array[i])
        meanAndReturn(array)
    print("--- %s seconds --- for test:" % (time.time() - start_time),j)

def saGeneralTest():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print("GENERAL SA TEST")
    
    
    start_time = time.time()
    for j in range(60):
        array=[]
        for i in range(10):
            array.append([])
            algo=SA()
            algo.setAircraftsSet(aircraftSetObject.set[j])
            result=algo.SAert(160,0.95,4,array[i])
        meanAndReturn(array)
    print("--- %s seconds --- for test:" % (time.time() - start_time),j)
 

def mrChangeProbTest():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print("CHANGE PROB CHANGE TEST")

    changeProb=0.1
    for k in range(5):
        print("LOOP:",5000,"CHANGE PROB:",changeProb)
        start_time = time.time()
        for j in range(20):
            array=[]
            for i in range(10):
                array.append([])
                algo=metaRaps()
                algo.setAircraftsSet(aircraftSetObject.set[j])
                result=algo.metaRapsAatcsr(changeProb,5000,array[i])
            meanAndReturn(array)
        print("--- %s seconds --- for test:" % (time.time() - start_time),j)
        changeProb+=0.05  

def mrGeneralTest():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print("GENERAL METARAPS TEST")

    
    start_time = time.time()
    for j in range(60):
        array=[]
        for i in range(10):
            array.append([])
            algo=metaRaps()
            algo.setAircraftsSet(aircraftSetObject.set[j])
            result=algo.metaRapsErt(0.2,5000,array[i])
        meanAndReturn(array)
    print("--- %s seconds --- for test:" % (time.time() - start_time),j)

def aatcsrGeneralTest():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print ("GENERAL AATCSR TEST")

    start_time = time.time()
    for i in range(60):
        algo=AATCSR()
        algo.setAircraftsSet(aircraftSetObject.set[i])
        print(int(algo.AATCSR()[0]))

def fpiGeneralTest():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print ("GENERAL FPI TEST")

    start_time = time.time()
    for i in range(60):
        algo=FPI()
        algo.setAircraftsSet(aircraftSetObject.set[i])
        print(int(algo.FPI()[0]))

def ertGeneralTest():
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    print ("GENERAL ERT TEST")

    start_time = time.time()
    for i in range(60):
        algo=ERT()
        algo.setAircraftsSet(aircraftSetObject.set[i])
        print(int(algo.ERT()[0]))

def runSA(index,which):
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    algo=SA()
    array=[]
    algo.setAircraftsSet(aircraftSetObject.set[index])
    result=[]
    if(which==0):
        result=list(algo.SAaatcsr(160,0.95,4,array))
    if(which==1):
        result=list(algo.SAfpi(160,0.95,4,array))
    if(which==2):
        result=list(algo.SAert(160,0.95,4,array))
    startTimeList=algo.findStartTime(result[1],0)[1]
    for i in range(len(startTimeList)):
        startTimeList[i]*=60
    result.append(startTimeList)
    return result

def runGA(index):
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    algo=GA()
    array=[]
    algo.setAircraftsSet(aircraftSetObject.set[index])
    result=list(algo.GAWithLocalSearch(60,800,1000,array,0.8))
    startTimeList=algo.findStartTime(result[1],0)[1]
    for i in range(len(startTimeList)):
        startTimeList[i]*=60
    result.append(startTimeList)
    return result

def runMetaRaps(index,which):
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")
    algo=metaRaps()
    array=[]
    algo.setAircraftsSet(aircraftSetObject.set[index])
    result=[]
    if(which==0):
        result=list(algo.metaRapsAatcsr(0.2,5000,array))
    if(which==1):
        result=list(algo.metaRapsFpi(0.2,5000,array))
    if(which==2):
        result=list(algo.metaRapsErt(0.2,5000,array))
    startTimeList=algo.findStartTime(result[1],0)[1]
    for i in range(len(startTimeList)):
        startTimeList[i]*=60
    result.append(startTimeList)
    return result

def runAATCSR(index):
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")

    algo=AATCSR()
    algo.setAircraftsSet(aircraftSetObject.set[index])
    res=algo.AATCSR()
    result=[]
    result.append(res[0])
    result.append(res[2])
    result.append(algo.findStartTime(result[1],0)[1])
    for i in range(len(result[2])):
        result[2][i]*=60
    
    return result

def runFPI(index):
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")

    algo=FPI()
    algo.setAircraftsSet(aircraftSetObject.set[index])
    res=algo.FPI()
    result=[]
    result.append(res[0])
    result.append(res[2])
    result.append(algo.findStartTime(result[1],0)[1])
    for i in range(len(result[2])):
        result[2][i]*=60
    
    return result

def runERT(index):
    aircraftSetObject = AircraftsSet()
    aircraftSetObject.readDataSet("data_set.txt")

    algo=ERT()
    algo.setAircraftsSet(aircraftSetObject.set[index])
    res=algo.ERT()
    result=[]
    result.append(res[0])
    result.append(res[2])
    result.append(algo.findStartTime(result[1],0)[1])
    for i in range(len(result[2])):
        result[2][i]*=60
    
    return result
    

def main():
    
    seed(datetime.now())
    for i in range(60):
        print("Test",i)
        print("AATCSR:",runAATCSR(i)[0])
        print("FPI:",runFPI(i)[0])
        print("ERT:",runERT(i)[0])
        print("SAaatcsr:",runSA(i,0)[0])
        print("SAfpi:",runSA(i,1)[0])
        print("SAert:",runSA(i,2)[0])
        print("MRaatcsr:",runMetaRaps(i,0)[0])
        print("MRfpi:",runMetaRaps(i,1)[0])
        print("MRert:",runMetaRaps(i,2)[0])
        print("GA:",runGA(i)[0])
        print('')


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
