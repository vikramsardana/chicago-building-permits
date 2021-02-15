import pandas as pd
from _ast import Str
from builtins import str

buildingDataTrimmed = None
buildingDataPositiveUnpaid = None
buildingDataNegativeUnpaid = None
permitTypes = ["ELECTRIC WIRING", "EASY PERMIT PROCESS", "RENOVATION/ALTERATION", "SIGNS", "NEW CONSTRUCTION", "WRECKING/DEMOLITION", "ELEVATOR EQUIPMENT",
                 "SCAFFOLDING", "REINSTATE REVOKED PMT", "FOR EXTENSION OF PMT", "PORCH CONSTRUCTION"]


def getInput(text):
    return str(input(text))

    
def getBayesianPermitTypeGivenBalanceAmount(permitType, posNeg, balanceType):
    balanceType = "SUBTOTAL_" + balanceType
    allBuildingData = pd.read_csv('building_permits_trimmed.csv')
    totalPermits = allBuildingData.shape[0]
    buildingDataSpecificPermit = allBuildingData.loc[allBuildingData['PERMIT_TYPE'] == permitType]
    totalSpecificPermit = buildingDataSpecificPermit.shape[0]
    if totalSpecificPermit == 0:
        return 0    
    buildingDataPosNeg = None
    buildingDataSpecificPermitPosNeg = None
    if posNeg == 1:
        buildingDataPosNeg = allBuildingData[allBuildingData[balanceType] > 0]
        buildingDataSpecificPermitPosNeg = buildingDataSpecificPermit[buildingDataSpecificPermit[balanceType] > 0]
        
    if posNeg == 0:
        buildingDataPosNeg = allBuildingData[allBuildingData[balanceType] == 0]
        buildingDataSpecificPermitPosNeg = buildingDataSpecificPermit[buildingDataSpecificPermit[balanceType] == 0]
        
    if posNeg == -1:
        buildingDataPosNeg = allBuildingData[allBuildingData[balanceType] < 0]
        buildingDataSpecificPermitPosNeg = buildingDataSpecificPermit[buildingDataSpecificPermit[balanceType] < 0]
        
    totalPosNeg = buildingDataPosNeg.shape[0]
    totalSpecificPermitPosNeg = buildingDataSpecificPermitPosNeg.shape[0]
    probB = float(totalPosNeg / totalPermits)
    if probB == 0.00000:
        return None
    probBGivenA = float(totalSpecificPermitPosNeg / totalSpecificPermit)
    probA = float(totalSpecificPermit / totalPermits)
    bayesianValue = (probBGivenA * probA) / probB
    return bayesianValue

def printFrequencies(balanceType, posNeg):
    allBuildingData = pd.read_csv('building_permits_trimmed.csv')
    balanceType = balanceType.upper()
    if balanceType == "ALL":
        print(allBuildingData['PERMIT_TYPE'].value_counts())
        return
    balanceType = "SUBTOTAL_" + balanceType
    balanceType = balanceType.upper()
    buildingDataPosNeg = None
    if posNeg == 1:
        buildingDataPosNeg = allBuildingData[allBuildingData[balanceType] > 0]
        
    if posNeg == 0:
        buildingDataPosNeg = allBuildingData[allBuildingData[balanceType] == 0]
        
    if posNeg == -1:
        buildingDataPosNeg = allBuildingData[allBuildingData[balanceType] < 0]
    print(buildingDataPosNeg['PERMIT_TYPE'].value_counts())

if __name__ == '__main__':
    while True:
        print(" ")
        print("===============================")
        print(" ")
        command = getInput("What do you want to do?\nCommands are Bayesian, Frequencies, or exit/quit.\n")
        if command.upper() == "QUIT" or command.upper() == "EXIT":
            print("OK! Thank you for exploring!")
            break        
        elif command.upper() == "BAYESIAN":
            permitType = getInput("Please enter the permit type from the following list. We suggest copy and pasting. " + str(permitTypes) + "\n")
            permitType = "PERMIT - " + permitType
            permitType = permitType.upper()
            given = getInput("Please enter what you want the condition to be. You can based it on unpaid amounts (say Unpaid), paid amount (say Paid), waived amount (say Waived)\n")
            given = given.upper()
            posNeg = int(getInput("Do you want it based on having a positive balance (say 1), a negative balance (say -1), or no balance (say 0)?\n"))
            bayesianValue = getBayesianPermitTypeGivenBalanceAmount(permitType, posNeg, given)
            if bayesianValue == None:
                print("Sorry, we couldn't find any permits with that " + given + " balance.\n")
            if bayesianValue == 0:
                print("Sorry, we couldn't find any permits of type " + permitType)
            else:
                print("The Bayesian probability of having a permit of type " + permitType + " with that " + given + " balance is " + str(bayesianValue))
        elif command.upper() == "FREQUENCIES":
            balanceType = getInput("Do you want the permit type frequencies of unpaid balances (say Unpaid), paid balances (say Paid), waived balances (say Waived), or all balances (say All)?\n")
            posNeg = 0
            if balanceType.upper() != "ALL":
                posNeg = int(getInput("Do you want it based on having a positive balance (say 1), a negative balance (say -1), or no balance (say 0)?\n"))
            printFrequencies(balanceType, posNeg)
        else:
            print("Sorry, that's not a valid command.\n")