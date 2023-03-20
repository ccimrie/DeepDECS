import sys
import os
import numpy as np
from operator import itemgetter
import library as lib

#run as:
#python deepDECSAugment.py model.pm k conf_mat.txt output_model.sm

#read parameters from console
try:
    simpleSystemFile=sys.argv[1]
except:
    "Not a valid file name"
confMFile=sys.argv[2] #confusion matrix file
outputFile=sys.argv[3] #name of the outputFile

stateVariable='k' #the 'k' state variable

#read confM
conf_mat_txt=np.loadtxt(confMFile)
conf_mat_shape=np.shape(conf_mat_txt)
verifMethods=int(np.log(conf_mat_shape[0]/conf_mat_shape[1])/np.log(2))

if verifMethods==0:
    confM=np.reshape(conf_mat_txt, (conf_mat_shape[1], conf_mat_shape[1]))
else:
    confM=np.reshape(conf_mat_txt, (np.power(2,verifMethods), conf_mat_shape[1], conf_mat_shape[1]))

currentModel=''#to recognise the model we are currently running and make appropiate tweaks
# currentModel=simpleSystemFile.split('.')[0]

#this is the main function
def generate():
    path=os.path.dirname(os.path.abspath(__file__))
    #load an copy the controller Template
    simple = open(path+"/"+simpleSystemFile, "r")
    augmented = path+"/"+outputFile
    content = simple.read()
    content_list = content.split("\n")

    posBegin=0
    posEnd=0
    posOk=0
    band=0
    #identify module EnvironmentMonitor
    for i in range(0,len(content_list)):
        if(content_list[i]=='module EnvironmentMonitor'):
            band=1
            posBegin=i
        #identify line of definition of state variable to be ovewritten
        if(content_list[i].strip().startswith(stateVariable)):
            posOk=i

        if(content_list[i]=='endmodule' and band==1):
            posEnd=i
            break

    #identify only EnvironmentMonitor module to extract actions and values of stateVariable
    system=content_list[posBegin:posEnd+1]

    #copy the module EnvironmentModule + header as it is in the simple-system
    region=content_list[0:posBegin]
    lib.writeInFile(augmented,region,"w")

    matrices=[]
    #first obtain the set of probs this is if verif methods=0
    if(verifMethods==0):
        probsPerClass=lib.extractMatrixProbs(confM)
        lib.writeInFile(augmented,probsPerClass,'a')
        #extract system check guards to then multiply each by the matrix probs
        finalLines=lib.extractChecks(system,stateVariable,confM,currentModel)#returns the new checks multiplied by the matrix probs
        newSystem=lib.assembleNewController(system,finalLines,len(confM[1]))
        lib.writeInFile(augmented,newSystem,'a')
        
        #identify module switch
        switch=lib.extractSwitchModule(content_list)
        lib.writeInFile(augmented,switch,'a')#add the switch module as it is
        #extract controller consts
        consts=lib.extractControllerConstsV2(content_list)
        lib.writeInFile(augmented,consts,'a')#add the constants
        #find the controller
        controller=lib.extractController(content_list,stateVariable)
        lib.writeInFile(augmented,controller,'a')#add the controller
        #find rewards
        rewards=lib.extractRewards(content_list)
        lib.writeInFile(augmented,rewards,'a')#add the rewards

    elif(verifMethods>=1):
        '''to avoid manually insering the matrices as potentially we could have many (or maybe not) I will supose 
        there exist n conf matrices named confusionMatrix_n.
        So for 1 verifMethod the names of the files will be confusionMatrix_0 (verif Matrix) and confusionMatrix_1 (non verif)'''
        matrices=[m for m in confM]
        #extract the probs from the verif matrices
        pVerifConsts,pVerifWhenClassConsts=lib.extractMatrixProbsVerif(matrices)
        lib.writeInFile(augmented,pVerifConsts,'a')
        lib.writeInFile(augmented,pVerifWhenClassConsts,'a')

        #extract checks verified
        finalLines=lib.extractChecksVerif(system,stateVariable,matrices,currentModel)#returns the new checks multiplied by the matrix probs
        # finalLines[0]=finalLines[0].replace('+', '+\n  ')

        newSystem=lib.assembleNewControllerVerif(system,finalLines,len(matrices[1]),len(matrices))
        lib.writeInFile(augmented,newSystem,'a')

        #identify module switch
        switch=lib.extractSwitchModule(content_list)
        switch.append('')#add just a space
        lib.writeInFile(augmented,switch,'a')#add the switch module as it is

        #extract controller consts
        consts=lib.extractControllerConstsV2(content_list)
        #clean consts as it has potentially some spaces
        consts = [string for string in consts if string != ""]
        controller=lib.writeControllerModuleWithVerificationV2(content_list,matrices,stateVariable,consts,currentModel)
        lib.writeInFile(augmented,controller,'a')#add the controller
        #find rewards
        rewards=lib.extractRewards(content_list)
        lib.writeInFile(augmented,rewards,'a')#add the rewards   

if __name__ == "__main__":
    generate()