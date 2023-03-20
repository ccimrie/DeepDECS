#This library contains all the functions that will be required to generate the augmented controller
import sys
import os
import numpy as np
from operator import itemgetter
import itertools

def writeInFile(file,alist,mode):
    textfile = open(file, mode)
    for element in alist:
        textfile.write(element + "\n")
    textfile.close()

def readConfusionMatrix(file):
    confM = np.loadtxt(file, dtype='i', delimiter=',')
    return confM

def writeDnnModule(confM,file,stateVariable):
    probs = np.zeros(shape=confM.shape)
    shape=confM.shape
    shape=shape[0]
    for row in range(0,confM.shape[0]):
        total=sum(confM[row]).item()
        for col in range(0,confM.shape[1]):
            probs[row][col]=float(confM[row][col].item())/total

    #define probabilities 
    rDNNVar='\nconst double rDNN = 20;'
    probsPerClass=[]
    probsPerClass.append(rDNNVar)
    for row in range(0,probs.shape[0]):
        probsPerClass.append('')#this adds a line between blocks of probs
        for col in range(0,probs.shape[1]):
            probsPerClass.append('const double pClass'+str(row)+'AsClass'+str(col)+'='+str(probs[row][col])+';')
            #print('const double pClass'+str(row)+'AsClass'+str(col)+'='+str(probs[row][col])+';')
    #okPrediction
    #define dnn module
    moduleDnn=[]
    moduleDnn.append('\nmodule DNN')
    moduleDnn.append('  '+stateVariable+'Prediction : [0..'+str(shape-1)+'] init 1;')
    
    for row in range(0,probs.shape[0]):
        moduleDnn.append('')
        for col in range(0,probs.shape[1]):
            moduleDnn.append('  [predict'+str(col)+'] '+stateVariable+'='+str(row)+' -> rDNN * pClass'+str(row)+'AsClass'+str(col)+' : ('+stateVariable+'Prediction\'='+str(col)+');')
    moduleDnn.append('endmodule\n')

    writeInFile(file,probsPerClass,"a")
    writeInFile(file,moduleDnn,"a")

def writeDnnModuleWithVerification(matrices,file,stateVariable):
    shape=matrices[0].shape#all matrices must have the same shape
    shape=shape[0]
    #pClass0AsClass0Verif
    #pClass0AsClass0NotVerif
    allProbs=[]#save the probabilities of each class
    for i in range(0,len(matrices)):
        probs = np.zeros(shape=matrices[i].shape)
        shape=matrices[i].shape
        shape=shape[0]
        for row in range(0,matrices[i].shape[0]):
            total=sum(matrices[i][row]).item()
            for col in range(0,matrices[i].shape[1]):
                probs[row][col]=float(matrices[i][row][col].item())/total
        allProbs.append(probs)

    #extract the probs and define the array
    pVerifWhenClassConsts=[]   
    for i in range(0,len(allProbs)):
        pVerifWhenClassConsts.append('')
        for row in range(0,allProbs[i].shape[0]):
            for col in range(0,allProbs[i].shape[1]):
                #print('const double pClass'+str(row)+'asClass'+str(col)+'Verif'+str(i)+' = '+str(allProbs[i][row][col]))
                pVerifWhenClassConsts.append('const double pClass'+str(row)+'AsClass'+str(col)+'Verif'+str(i)+' = '+str(allProbs[i][row][col])+';')

    #calculate verified probabilities. this case only works for 1 verif method
    #probsVerif = np.zeros(shape=matrices[0].shape)
    nums=[]
    denom=[0]*matrices[0].shape[0]#the shape of any matrix is the shape of all matrices
    #denoms=[]
    for i in range(0,len(matrices)):
        num=[]
        for row in range(0,matrices[i].shape[0]):#row is class
            #print('mat'+str(i)+str(row),sum(matrices[i][row]).item())
            '''
            e.g. if verif methods=1
            m1=[[710,20],[15,590]]
            m2=[[160,110],[135,260]]
            
            2 numerators will be sharing the same denominator 
            710+20/710+20+160+110
            160+110/710+20+160+110
            '''
            num.append(sum(matrices[i][row]).item())#store the sum of rows per class in matrix i e.g.[[710+20],[15+590]]
            denom[row]+=(sum(matrices[i][row]).item())#will be storing num in pos row of matrices e.g. [[710+20+160+110],[15+590+135+260]]
        nums.append(num)

    pVerifConsts=[]

    pVerifConsts.append('')
    rDNNVar='\nconst double rDNN = 20;'
    pVerifConsts.append(rDNNVar)
    pVerifConsts.append('')
    for i in range(0,len(nums)):#i represents the no of matrix
        for j in range(0,len(nums[i])):#j represents the class
            #print("pVerif"+str(i)+'WhenClass'+str(j),nums[i][j],'/',denom[j],float(nums[i][j])/denom[j])
            pVerifConsts.append('const double pVerif'+str(i)+'WhenClass'+str(j)+' = '+str(float(nums[i][j])/denom[j])+';')

    #write module dnn the module will have K*2^n*K lines where K is the num of classes and n is the num of verif methods e.g. 2*2*2
    moduleDnn=[]
    moduleDnn.append('\nmodule DNN')
    moduleDnn.append('  '+stateVariable+'Prediction : [0..'+str(shape-1)+'] init 1;')
    moduleDnn.append('  predictionVerified : [0..'+str(len(matrices)-1)+'] init 1;')#predictionVerified is one val per matrix e.g. [00] or [0000]

    for i in range(0,len(matrices)):#Verif matrix i
        moduleDnn.append('')
        for row in range(0,matrices[i].shape[0]):#actual class
            for col in range(0,matrices[i].shape[1]):#predicted class
                #print('[predict'+str(col)+'Verif'+str(i)+'] '+stateVariable+'='+str(row)+' -> rDNN*pVerif'+str(i)+'WhenClass'+str(row)+'*pClass'+str(row)+'AsClass'+str(col)+'Verif'+str(i)+' : ('+stateVariable+'Prediction\'='+str(col)+')&(predictionVerified\'='+str(i)+');')
                moduleDnn.append('  [predict'+str(col)+'Verif'+str(i)+'] '+stateVariable+'='+str(row)+' -> rDNN*pVerif'+str(i)+'WhenClass'+str(row)+'*pClass'+str(row)+'AsClass'+str(col)+'Verif'+str(i)+' : ('+stateVariable+'Prediction\'='+str(col)+')&(predictionVerified\'='+str(i)+');')
    moduleDnn.append('endmodule\n')
    '''for i in range(0,len(pVerifConsts)):
        print(pVerifConsts[i])

    for i in range(0,len(pVerifWhenClassConsts)):
        print(pVerifWhenClassConsts[i])

    for i in range(0,len(moduleDnn)):
        print(moduleDnn[i])'''
    writeInFile(file,pVerifConsts,"a")
    writeInFile(file,pVerifWhenClassConsts,"a")
    writeInFile(file,moduleDnn,"a")



def extractControllerConsts(content_list):
    band=0
    #begin and end of const doubles
    begin=0
    end=0
    for i in range(0,len(content_list)):
        if(content_list[i]=='module System' or content_list[i]=='module Robot'):
            band=1
        if(content_list[i]=='endmodule' and band==1):
            #found end of module so from next line on you will find consts
            begin=i+1
            break
    for i in range(0,len(content_list)):
        if(content_list[i]=='module Controller'):
            end=i
            break
    constVals=[]
    for i in range(begin,end):
        if(content_list[i]!='' and '//' not in content_list[i]):
            constVals.append(content_list[i])

    return constVals



def writeControllerModule(confM,file,varInController,final,constVals):
    #missing I need to identify the defintion of the variable warning : bool init false; in controller to use this same name assign to varInController
    shape=confM.shape
    shape=shape[0]
    moduleController=[]

    #add first the controller constants
    moduleController=moduleController+constVals

    #define controller module
    moduleController.append('\nmodule Controller')
    #moduleController.append('  '+varInController+' : [0..'+str(shape-1)+'] init 3;')
    moduleController.append(varInController)
    moduleController.append('')

    #sort final
    final=sorted(final, key=itemgetter(1))#final has the shape [[action,system_value,predicate]]

    controllerLines=[]
    #add first element of each line e.g. [predict1]
    for i in range(0,len(final)):
        controllerLines.append('  [predict'+str(final[i][1])+'] true -> '+final[i][2])
    
    '''#complete each of the lines e.g. [predict1]+x11+x12+..x17
    for i in range(0,len(controllerLines)):
        cad=''
        for col in range(0,confM.shape[1]):
            if(col==confM.shape[1]-1):#if is the last line
                cad=cad+'x'+str(i)+str(col)+':('+varInController+'\'='+str(col)+');'
            else:
                cad=cad+'x'+str(i)+str(col)+':('+varInController+'\'='+str(col)+') + '
        #add the line to controller lines
        controllerLines[i]=controllerLines[i]+cad'''
    #combine lists
    moduleController=moduleController+controllerLines
    moduleController.append('endmodule\n')
    #write in the augmented controller
    writeInFile(file,moduleController,"a")


def writeControllerModuleWithVerification(matrices,file,varInController,final,constVals):
    #missing I need to identify the defintion of the variable warning : bool init false; in controller to use this same name assign to varInController
    shape=matrices[0].shape#all matrices must have the same shape
    shape=shape[0]
    moduleController=[]

    #modify the constVars to add nowOne var per conf matrix
    augmentedConstVals=[]# add the const vals per conf matrix
    names=[]
    for i in range(0,len(constVals)):
        #extract name of constant
        name=constVals[i].split(' ')[2]
        name=name.split(';')[0]#remove ; to get clean name
        names.append(name)

    replacements=[]
    for i in range(0,len(names)):
        oneRep=[]
        for j in range(0,len(matrices)):
            #print('const double '+names[i]+'Verif'+str(j)+';')
            augmentedConstVals.append('const double '+names[i]+'Verif'+str(j)+';')
            oneRep.append(names[i]+'Verif'+str(j))
        replacements.append(oneRep)#save the names of vars to then replace

    #add first the controller constants
    moduleController=moduleController+augmentedConstVals

    #define controller module
    moduleController.append('\nmodule Controller')
    #moduleController.append('  '+varInController+' : [0..'+str(shape-1)+'] init 3;')
    moduleController.append(varInController)
    moduleController.append('')

    #sort final
    final=sorted(final, key=itemgetter(1))#final has the shape [[action,system_value,predicate]]


    #create chunks in name of size n, the size comes from how many states are there in varInController
    n = int(varInController.split('..')[1][0])+1#this will hopefully give the size of chunks
    # using list comprehension 
    names = [names[i:i + n] for i in range(0, len(names), n)]


    #add first element of each line e.g. [predict1]
    finalGuards=[]

    for j in range(0,len(final)):
            #for k in range(0,len(matrices)):
                #print(final[j][2])
                #print(names[j])
                finalGuards.append(replace(final[j][2],names[j],matrices))
                #print(names[i][j])
                #print(final[i][2].replace(names[i][j],names[i][j]+'Verfi'))
    
    finalGuards = [item for sublist in finalGuards for item in sublist]

    finalActions=[]
    for i in range(0,len(final)):
        for j in range(0,len(matrices)):
            #print('  [predict'+str(final[i][1])+'Verif'+str(j)+']')
            finalActions.append('  [predict'+str(final[i][1])+'Verif'+str(j)+']')

    
    controllerLines=[]
    #create the controller lines
    for i in range(0,len(finalActions)):
        #print(finalActions[i]+ ' true -> '+finalGuards[i])
        controllerLines.append(finalActions[i]+' true -> '+finalGuards[i])

    moduleController=moduleController+controllerLines
    moduleController.append('endmodule\n')
    #write in the augmented controller
    writeInFile(file,moduleController,"a")


def replace(string,vals,matrices):
    #print('in replace')
    final=[]
    for j in range(0,len(matrices)):
        scopy=string
        for i in range(0,len(vals)):
            scopy=scopy.replace(vals[i],vals[i]+'Verif'+str(j))
        final.append(scopy)
    return final
          

def identifyControllerInSimple(content_list,final):
    stateVariable=''
    start=0
    end=0
    band=0
    for i in range(0,len(content_list)):
        if(content_list[i]=='module Controller'):
            band=1
            start=i
            #stateVariable=content_list[i+1]#state variable is just after the begining of the module
        if(band==1 and content_list[i]=='endmodule'):
            end=i
            break
    #identify state variable, is the first text line after opening
    for i in range(start,end+1):
        if(content_list[i]!='module Controller' and content_list[i]!=''):
            #stateVariable=content_list[i].strip().split(':')
            stateVariable=content_list[i]
            break

    #extract only the module controller
    controller=content_list[start:end+1]
    #identify when actions in the controller start
   
    beginActions=0
    for i in range(0,end+1):
        if(controller[i].strip().startswith('[')):
            beginActions=i
            break
    #go through the controller to extract the predicates
    #there must be a match between unique actions in controller and system
    
    #extract from controller actions and predicates
    contActionAndPredicates=[]
    for i in range(beginActions,len(controller)-1):
        sentence=controller[i].strip()
        if(sentence!='' and '//' not in sentence):
            beginSubS=0
            for j in range(0,len(sentence)):
                if(sentence[j]=='['):
                    beginAction=j+1
                if(sentence[j]==']'):
                    endAction=j
            contActionAndPredicates.append([sentence[beginAction:endAction],sentence.split('->')[1]])#add action, predicate of controller
    
    #this code makes the assumption that thjere is only one predicate per action always 
    for i in range(0,len(final)):
        for j in range(0,len(contActionAndPredicates)):
            if(final[i][0]==contActionAndPredicates[j][0]):
                final[i].append(contActionAndPredicates[j][1])

    return stateVariable,final

def identifyRewards(content_list):
    start=0
    end=0
    band=0
    howMany=[]
    for i in range(0,len(content_list)):
        if(content_list[i].startswith('rewards')):
            howMany.append(i)
        if(content_list[i].startswith('endrewards')):
            howMany.append(i)

    rewardsText=content_list[howMany[0]:howMany[(len(howMany)-1)]+1]
    return rewardsText
            
def extractStatesAndActionsFromSystem(system,stateVariable):
    beginActions=0
    for i in range(0,len(system)):
        if(system[i].strip().startswith('[')):
            beginActions=i
            break

    #identify only the actions and vals in the system
    data=[]
    for i in range(beginActions,len(system)-1):
        sentence=system[i].strip()
        if(sentence!='' and '//' not in sentence):#this validation avoids error is there is \n between sentences and omits any comments
            beginSubS=0
            for j in range(0,len(sentence)):
                if(sentence[j]=='['):
                    beginAction=j+1
                if(sentence[j]==']'):
                    endAction=j
                if(sentence[j]=='\''):#concentrate on identifying  the pos with "'", eg "ok'=1);" in pos 2 is '
                    beginSubS=j

            #subS contains "'=1);", now identify the int in this string
            subS=sentence[beginSubS:len(sentence)-1]
            digit=''# need this as might be an n digits number
            for m in range(0,len(subS)):
                if(subS[m].isdigit()):
                    digit+=subS[m]
            data.append(sentence[beginAction:endAction]+'_'+digit)

    list_set = set(data)#when convert to set gives unique values
    data=list(list_set)

    copy= data[:]#copy the list data
    #validation to check "event associated with multiple new values"
    allRep=[]#save all repetitions
    while len(copy)>0:
        crrt=copy.pop(0)
        word=crrt.split('_')[0]#extract only the word
        rep=[]
        rep.append(crrt)
        for i in range(0,len(copy)):
            if copy[i].startswith(word):
                rep.append(copy[i])
        allRep.append(rep)
    # so far all repetitions are grouped, need to find if the len of a pos in allRep >1 then send the error
    errors=[]
    for i in range(0,len(allRep)):
        if(len(allRep[i])>1):
            errors.append(allRep[i])
    if(errors):
        print("Event(s) associated with multiple new values:")
        print(errors)
        sys.exit()
    
    final=[]
    for i in range(0,len(data)):
        vals=data[i].split('_')
        final.append([vals[0],int(vals[1])])

    return final

def findModuleAfterController(content_list):
    band=0
    begin=0#begin end of controller
    for i in range(0,len(content_list)):
        if (content_list[i]=='module Controller'):
            band=1
        if(content_list[i]=='endmodule' and band==1):
            begin=i+1
            break

    #find begin of first rewards
    beginRewards=0
    for i in range(0,len(content_list)):
        if (content_list[i].startswith('rewards')):
            beginRewards=i
            break

    #return the region of interest
    return content_list[begin:beginRewards]

#****************Functions for V2 models

def extractMatrixProbs(confM):
    probs = np.zeros(shape=confM.shape)
    shape=confM.shape
    shape=shape[0]
    for row in range(0,confM.shape[0]):
        total=sum(confM[row]).item()
        for col in range(0,confM.shape[1]):
            probs[row][col]=float(confM[row][col].item())/total

    probsPerClass=[]
    for row in range(0,probs.shape[0]):
        #probsPerClass.append('')#this adds a line between blocks of probs
        for col in range(0,probs.shape[1]):
            probsPerClass.append('const double pClass'+str(row)+'AsClass'+str(col)+'='+str(probs[row][col])+';')

    probsPerClass.append('')#this adds a line between blocks of probs
    return probsPerClass

def extractChecks(system,stateVariable,matrix,currentModel):
    namesVars=[]
    for row in range(0,matrix.shape[0]):
        oneRow=[]
        for col in range(0,matrix.shape[1]):
            oneRow.append('pClass'+str(row)+'AsClass'+str(col))
        namesVars.append(oneRow)

   #extract guards per line and store them as [[(1-pFail):(s'=1),pFail:(s'=2);]] and each pos (1-pFail) corresponds to one row in names i.e. correwsponds to 2 names
    guards=[]
    beginingGuard=[]
    for i in range(0,len(system)):
        if('check' in system[i] or 'monitor' in system[i]):
            a=system[i].split('->')#a[0] contains the begining of each guard
            beginingGuard.append(a[0])
            b=a[1].strip().split('+')
            guards.append(b)

    

    #match each guard element with each matrix row
    allNewGuards=[]
    for i in range(0,len(guards)):
        lenG=len(guards[i])
        if(lenG!=matrix.shape[0]):#this validation is because robot has one more line in the guard after '+' than rows in the matrix
            #originalLeng=lenG
            lenG=lenG-1
        oneNew=[]
        for j in range(0,lenG):#per line in check
            for k in range(0,len(namesVars[j])):#namesVars must be same lenght as lenG
                v=guards[i][j].split(':')#split by :

                oneNew.append(v[0].strip()+'*'+namesVars[j][k]+':'+v[1].strip().split(';')[0]+'&(k2\'='+str((k+1))+')')
                #print(v[0]+'*'+namesVars[j][k]+':'+v[1]+'&(z\'='+str((k+1))+')')
        allNewGuards.append(oneNew)
    

    finalLines=[]

    for i in range(0,len(allNewGuards)):#all new guards must be same lenght as beginingGuard
        l=''
        l+=beginingGuard[i]+'-> '
        for j in range(0,len(allNewGuards[i])):
            if(j+1<len(allNewGuards[i])):
                l+=allNewGuards[i][j]+'+'
            else:
                l+=allNewGuards[i][j]+';'
        finalLines.append(l)


    if(currentModel=='robot'):#if the model is robot add at the end +(1-pColliderPresent):(s'=2);
        finalLines[0]=finalLines[0].replace(";", "+(1-pColliderPresent):(s'=2);")
    return finalLines

def assembleNewController(system,finalLines,shape):
    firstCheck=0
    for i in range(0,len(system)):
        if('check' in system[i] or 'monitor' in system[i]):
            firstCheck=i#beginnes first check
            break
    defineZ='  k2 : [1..'+str(shape)+'] init 1;'
    system.insert(firstCheck-1,defineZ)
    
    toReplace=[]
    for i in range(0,len(system)):
        if('check' in system[i] or 'monitor' in system[i]):
            toReplace.append(i)
    
    #the same number of checks in system must correspond to the same numb of checks in the fina lines
    for i in range(0,len(toReplace)):
        system[toReplace[i]]=finalLines[i]
    system.append('')
    return system#new augmentes system


def extractSwitchModule(content_list):
    beginS=0
    endS=0
    band=0
    bandSwitch=0#to identify if the switch module is present as some models may not have this module
    for i in range(0,len(content_list)):
        if(content_list[i]=='module Switch'):
            beginS=i
            band=1
            bandSwitch=1
        if(content_list[i]=='endmodule' and band==1):
            endS=i
            break
    if(bandSwitch==1):
        switch=content_list[beginS:endS+1]
    else:
        switch=['']#no switch module found
    return switch

def extractControllerConstsV2(content_list):

    #this might come after the switch module for robot or after the environemnt monitor module for car
    #to generalise we need to define where these varibles will always be found in the model!!
    beginC=0
    endS=0
    band=0
    bandSwitch=0
    #identify end of switch
    for i in range(0,len(content_list)):
        if(content_list[i].strip()=='module Switch'):
            band=1
            bandSwitch=1 #switch module present
        if(content_list[i].strip()=='endmodule' and band==1):
            endS=i
            break

    #if module switch present then locate the constants

    if(bandSwitch==1):
        for i in range(0,len(content_list)):
            if(content_list[i].strip()=='module Controller'):
                beginC=i
                break
        consts=content_list[endS+1:beginC]

    elif(bandSwitch==0):
        for i in range(0,len(content_list)):
            if(content_list[i].strip()=='module EnvironmentMonitor'):
                band=1
            if(content_list[i].strip()=='endmodule' and band==1):
                endS=i
                break

        for i in range(0,len(content_list)):
            if(content_list[i].strip()=='module Controller'):
                beginC=i
                break
        consts=content_list[endS+1:beginC]
    return consts

def extractController(content_list,stateVariable):
    beginC=0
    endC=0
    band=0
    for i in range(0,len(content_list)):
        if(content_list[i]=='module Controller'):
            beginC=i
            band=1
        if(content_list[i]=='endmodule' and band==1):
            endC=i
            break

    controller=content_list[beginC:endC+1]
    #replace controller varible with z
    for i in range(0,len(controller)):
        if(stateVariable+'=' in controller[i]):
            controller[i]=controller[i].replace(stateVariable+'=','k2=')
    return controller

def extractRewards(content_list):
    beginC=0
    endC=0
    band=0
    for i in range(0,len(content_list)):
        if(content_list[i]=='module Controller'):
            beginC=i
            band=1
        if(content_list[i]=='endmodule' and band==1):
            endC=i
            break

    rewards=content_list[endC+1:len(content_list)]
    return rewards

def extractMatrixProbsVerif(matrices):
    shape=matrices[0].shape#all matrices must have the same shape
    shape=shape[0]
    #pClass0AsClass0Verif
    #pClass0AsClass0NotVerif
    allProbs=[]#save the probabilities of each class
    for i in range(0,len(matrices)):
        probs = np.zeros(shape=matrices[i].shape)
        shape=matrices[i].shape
        shape=shape[0]
        for row in range(0,matrices[i].shape[0]):
            total=sum(matrices[i][row]).item()

            for col in range(0,matrices[i].shape[1]):
                if(total==0):
                    probs[row][col]=0
                else:
                    probs[row][col]=float(matrices[i][row][col].item())/total
        allProbs.append(probs)

    #extract the probs and define the array
    pVerifWhenClassConsts=[]   
    for i in range(0,len(allProbs)):
        pVerifWhenClassConsts.append('')
        for row in range(0,allProbs[i].shape[0]):
            for col in range(0,allProbs[i].shape[1]):
                #print('const double pClass'+str(row)+'asClass'+str(col)+'Verif'+str(i)+' = '+str(allProbs[i][row][col]))
                pVerifWhenClassConsts.append('const double pClass'+str(row)+'AsClass'+str(col)+'Verif'+str(i)+' = '+str(allProbs[i][row][col])+';')

    #calculate verified probabilities.
    #probsVerif = np.zeros(shape=matrices[0].shape)
    nums=[]
    denom=[0]*matrices[0].shape[0]#the shape of any matrix is the shape of all matrices
    #denoms=[]
    for i in range(0,len(matrices)):
        num=[]
        for row in range(0,matrices[i].shape[0]):#row is class
            #print('mat'+str(i)+str(row),sum(matrices[i][row]).item())
            '''
            e.g. if verif methods=1
            m1=[[710,20],
                [15,590]]

            m2=[[160,110],
                [135,260]]
            
            2 numerators will be sharing the same denominator 
            710+20/710+20+160+110
            160+110/710+20+160+110
            '''
            num.append(sum(matrices[i][row]).item())#store the sum of rows per class in matrix i e.g.[[710+20],[15+590]]
            denom[row]+=(sum(matrices[i][row]).item())#will be storing num in pos row of matrices e.g. [[710+20+160+110],[15+590+135+260]]
        nums.append(num)

    pVerifConsts=[]

    pVerifConsts.append('')
    for i in range(0,len(nums)):#i represents the no of matrix
        for j in range(0,len(nums[i])):#j represents the class
            #print("pVerif"+str(i)+'WhenClass'+str(j),nums[i][j],'/',denom[j],float(nums[i][j])/denom[j])
            pVerifConsts.append('const double pVerif'+str(i)+'WhenClass'+str(j)+' = '+str(float(nums[i][j])/denom[j])+';')

    return pVerifConsts,pVerifWhenClassConsts

    
def extractChecksVerif(system,stateVariable,matrices,currentModel):
    shape=matrices[0].shape#all matrices must have the same shape
    shape=shape[0]
    #extract the probs and define the array
    classAsClassConsts=[]   
    for i in range(0,len(matrices)):
        oneMatrix=[]
        for row in range(0,shape):
            oneRow=[]
            for col in range(0,shape):
                #print('const double pClass'+str(row)+'asClass'+str(col)+'Verif'+str(i)+' = '+str(allProbs[i][row][col]))
                oneRow.append('pClass'+str(row)+'AsClass'+str(col)+'Verif'+str(i))
            oneMatrix.append(oneRow)
        classAsClassConsts.append(oneMatrix)

    #Extract VerifWhenClass consts
    pVerifConsts=[]
    for i in range(0,len(matrices)):#i represents the no of matrix
        oneMatrix=[]
        for j in range(0,shape):#j represents the class
            #print("pVerif"+str(i)+'WhenClass'+str(j),nums[i][j],'/',denom[j],float(nums[i][j])/denom[j])
            oneMatrix.append('pVerif'+str(i)+'WhenClass'+str(j))
        pVerifConsts.append(oneMatrix)

    #end variables names

    #extract guards per line and store them as [[(1-pFail):(s'=1),pFail:(s'=2);]] and each pos (1-pFail) corresponds to one row in names i.e. correwsponds to 2 names
    guards=[]
    beginingGuard=[]

    for i in range(0,len(system)):
        if('check' in system[i] or 'monitor' in system[i] ):
            a=system[i].split('->')#a[0] contains the begining of each guard
            beginingGuard.append(a[0])
            b=a[1].strip().split('+')
            guards.append(b)
    
    #multiply pverif by classAsClass probs 
    linesPerMatrix=[]
    for i in range(0,len(matrices)):#shape
        allLines=[]
        for j in range(0,len(classAsClassConsts[i])):
            oneLine=[]
            for k in range(0,len(classAsClassConsts[i][j])):
                #print(pVerifConsts[i][j],classAsClassConsts[i][j][k])
                oneLine.append(str(pVerifConsts[i][j])+'*'+str(classAsClassConsts[i][j][k]))
            allLines.append(oneLine)
        linesPerMatrix.append(allLines)

    #match the previous lines with the begining of the guard, e.g. pOK, pFail
    allMatrices=[]
    for k in range(0,len(linesPerMatrix)):#matrices
        perMatrix=[]
        for r in range(0,len(guards)):#this may throw an error?
            oneLine=[]
            for l in range(0,len(linesPerMatrix[k])):#per row
                for m in range(0,len(linesPerMatrix[k][l])):#per element in row
                    #pOk *   pVerif0WhenClass0 * pClass0AsClass0Verif0  :(s'=1)&(v'=0)&(z'=1)
                    v=guards[r][l].split(':')
                    #print(v[0].strip()+'*'+linesPerMatrix[k][l][m]+':'+v[1].strip().split(';')[0]+'&(v\'='+str(k)+')'+'&(z\'='+str(m+1)+')')
                    oneLine.append(v[0].strip()+'*'+linesPerMatrix[k][l][m]+':'+v[1].strip().split(';')[0]+'&(v\'='+str(k)+')'+'&(k2\'='+str(m+1)+')')
            perMatrix.append(oneLine)
        allMatrices.append(perMatrix)
    #just need to match each matrix with the beginingGuard !!
    #print(allMatrices)
    #print(beginingGuard)
    
    shapeList=len(allMatrices[0])#the shape of one list must be the shape of all lists
    group = [ [] for _ in range(shapeList) ]

    #group the set of guards 
    for j in range(0,len(allMatrices)):#per matrix
        for k in range(0,len(allMatrices[j])):
            group[k].append(allMatrices[j][k])
            #print(allMatrices[j][k])
    finalLines=[]
    for i in range(0,len(group)):#there should always be one group per beginig of guards
        flat = [item for sublist in group[i] for item in sublist]
        s=beginingGuard[i]
        s+='-> '
        for j in range(0,len(flat)):#go through each element in the list
            if(j+1<len(flat)):
                s+=flat[j]+'+'
            else:
                s+=flat[j]+';'
        finalLines.append(s)
    
    if(currentModel=='robot'):#if the model is robot add at the end +(1-pColliderPresent):(s'=2);
        finalLines[0]=finalLines[0].replace(";", "+(1-pColliderPresent):(s'=2);")
    return finalLines

def assembleNewControllerVerif(system,finalLines,shape,numMatrices):
    firstCheck=0
    for i in range(0,len(system)):
        if('check' in system[i] or 'monitor' in system[i]):
            firstCheck=i#begines firts check
            break
    defineZ='  k2 : [1..'+str(shape)+'] init 1;'
    defineV='  v : [0..'+str(numMatrices-1)+'] init 0;'

    system.insert(firstCheck-1,defineV)
    system.insert(firstCheck-1,defineZ)
    
    toReplace=[]
    for i in range(0,len(system)):
        if('check' in system[i] or 'monitor' in system[i]):
            toReplace.append(i)
    
    #the same number of checks in system must correspond to the same numb of checks in the fina lines
    for i in range(0,len(toReplace)):
        system[toReplace[i]]=finalLines[i]
    system.append('')
    return system#new augmentes system

def writeControllerModuleWithVerificationV2(content_list,matrices,stateVariable,constVals,currentModel):
    #missing I need to identify the defintion of the variable warning : bool init false; in controller to use this same name assign to varInController
    shape=matrices[0].shape#all matrices must have the same shape
    shape=shape[0]
    moduleController=[]

    #modify the constVars to add nowOne var per conf matrix
    augmentedConstVals=[]# add the const vals per conf matrix
    names=[]
    for i in range(0,len(constVals)):
        #extract name of constant
        name=constVals[i].split(' ')[2]
        name=name.split(';')[0]#remove ; to get clean name
        names.append(name)

    replacements=[]
    for i in range(0,len(names)):
        oneRep=[]
        for j in range(0,len(matrices)):
            #print('const double '+names[i]+'Verif'+str(j)+';')
            if(currentModel=='safeSCAD'):
                augmentedConstVals.append('const int '+names[i]+'Verif'+str(j)+';')
            else:
                augmentedConstVals.append('const double '+names[i]+'Verif'+str(j)+';')
            oneRep.append(names[i]+'Verif'+str(j))
        replacements.append(oneRep)#save the names of vars to then replace


    #add first the controller constants
    moduleController=moduleController+augmentedConstVals

    beginC=0
    endC=0
    band=0
    for i in range(0,len(content_list)):
        if(content_list[i].strip()=='module Controller'):
            beginC=i
            band=1
        if(content_list[i]=='endmodule' and band==1):
            endC=i
            break

    controller=content_list[beginC:endC+1]

    #replace controller varible with z
    for i in range(0,len(controller)):
        if(stateVariable+'=' in controller[i]):
            controller[i]=controller[i].replace(stateVariable+'=','k2=')
    
    guardsInControl=[]
    for i in range(0,len(controller)):
        if('respond' in controller[i] or 'decide' in controller[i]):
            guardsInControl.append(controller[i])

    finalGuards=[]
    for i in range(0,len(guardsInControl)):
        for j in range(0,len(replacements[i])):
            d=guardsInControl[i].split('->')
            d1=d[0]
            d2=d[1]
            d1+='& v='+str(j)+' -> '
            df=d1+d2
            #print(df.replace(names[i],replacements[i][j]))
            finalGuards.append(df.replace(names[i],replacements[i][j]))

    end=0
    for i in range(0,len(controller)):
        if('respond' in controller[i] or 'decide' in controller[i]):
            end=i
            break


    newController=[]
    newController.extend(augmentedConstVals)
    newController.append('')
    newController.extend(controller[0:end])
    newController.extend(finalGuards)
    newController.append('endmodule')

    return newController