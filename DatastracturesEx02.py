import copy
import random

#We keep classes of all the diffrenet parts of the queries in order to make it easeir to manipulate the query
class PI:
    attributesList = []
    name = "PI"

    def __init__(self):
        self.attributesList = []

class Sigma:
    conditionsList = []
    name = "Sigma"
    def __init__(self):
        self.conditionsList = []

class Cartesian:
    firstTable = []
    secondTable = []
    isNjoin = False
    name = "Cartesian"


    def __init__(self):
        self.firstTable = []
        self.secondTable = []
        isNjoin = False

class Njoin:
    firstTable = []
    secondTable = []

    def __init__(self):
        self.firstTable = []
        self.secondTable = []


def swapAndWithComma(sigma) -> str:
    sigma = sigma.replace("AND", ",")
    return sigma


def cleanCondition(condition) -> str:
    #We swap all the relation operators with comma, so it is easier to split a condition string
    #According to different rel ops
    condition = condition.replace("OR", ",")
    condition = condition.replace("AND", ",")
    condition = condition.replace(">=", ",")
    condition = condition.replace("<=", ",")
    condition = condition.replace("=", ",")
    condition = condition.replace(">", ",")
    condition = condition.replace("<", ",")
    return condition


def makeAttributesFromSigmas(sigma, tableR, tableS) -> list:
    attributes = []
    for condition in sigma.conditionsList:
        condition = cleanCondition(condition) 
        sigmaAttributes = condition.split(",")
        for attribute in sigmaAttributes:
            attribute = attribute.strip()
            if (attribute in tableS) or (attribute in tableR):
                attributes.append(attribute)

    return attributes

def makeAttributesFromCondition(condition, tableR, tableS) -> list:
    attributes = []
    condition = cleanCondition(condition)
    conditionAttributes = condition.split(",")
    for attribute in conditionAttributes:
        attribute = attribute.strip()
        if (attribute in tableS) or (attribute in tableR):
            attributes.append(attribute)

    return attributes


def makeConditionsFromSigmas(Sigmas) -> list:
    conditions = []
    for sigma in Sigmas:
        sigma = swapAndWithComma(sigma)
        conditions += str(sigma).split(",")

    stripedConditions = []
    for condition in conditions:
        stripedConditions.append(condition.replace(" ", ""))

    return stripedConditions

def clearBrackets(sigma)->Sigma:
    newSigma = Sigma()
    newCondition = sigma.conditionsList[0]
    newCondition = newCondition.replace("(", "")
    newCondition = newCondition.replace(")", "")
    newSigma.conditionsList.append(newCondition)

    return newSigma

#We split the sigma by the first "AND" we find
def splitSigmaByAND(sigma) -> list:
    tempStr = sigma
    index = str(tempStr).find("AND")
    if index!=-1:
         sigmas = [sigma[0:index], sigma[index + 3:]]
         return sigmas
    else: #If we couldn't find AND we return NONE (shouldn't happen because we check first we can execute this split)
         return None


def cleanString(mainString, substring):
    mainString = mainString[len(substring)::]
    mainString = mainString.strip(" ")
    return mainString


def printMenu(selectionOptions):
    print("Please choose one of the following options:")
    i = 1
    for option in selectionOptions:
        print(str(i) + ". " + option)
        i += 1


def isValidChoice(userChoice) -> bool:
    return userChoice.isnumeric() and 1 <= int(userChoice) and int(userChoice) <= 6


def canExecuteRule4(algebricExpression) -> bool:
    # We lay on the assumption that if the sigma block contains at least one "AND" we can use rule 4
    for item in algebricExpression:
        if type(item) is Sigma:
            for condition in item.conditionsList:
                if "AND" in condition:
                    return True
    return False


def canExecuteRule4a(algebricExpression) -> bool:
    for item in algebricExpression:
        if type(item) is Sigma:
            if len(item.conditionsList) >= 2:
                return True
    return False


def canExecuteRule5a(algebricExpression, tableR, tableS) -> bool:
    pi = PI()
    sigma = Sigma()
    foundPiSigma = False

    for i in range(len(algebricExpression)):
        if type(algebricExpression[i]) is PI:
            if i + 1 < len(algebricExpression):
                if type(algebricExpression[i + 1]) is Sigma:
                    pi = algebricExpression[i]
                    sigma = algebricExpression[i + 1]
                    foundPiSigma = True
                    break
    if foundPiSigma:
        attributes = makeAttributesFromSigmas(sigma, tableR, tableS)
        for attribute in attributes:
            if not attribute in algebricExpression[i].attributesList:
                return False
        return True
    return False


def canExecuteRule6(algebricExpression, tableR, tableS) -> bool:
    isAttributeFromR = False
    isAttributeFromS = False
    for item in algebricExpression:
        if type(item) is Sigma:
            for condition in item.conditionsList:
                attributes = makeAttributesFromCondition(condition,tableR,tableS)
                for attribute in attributes:
                    if attribute in tableR:
                        isAttributeFromR = True
                    if attribute in tableS:
                        isAttributeFromS = True
                if not (isAttributeFromS and isAttributeFromR):
                    return True
                else:
                    isAttributeFromR = False
                    isAttributeFromS = False
    return False

def canExecuteRule6a(Sigmas, tableR, tableS) -> bool:
    attributes = makeAttributesFromSigmas(Sigmas, tableR, tableS)
    for attribute in attributes:
        if not attribute in tableS:
            return False
    return True


def isTheRightConditionFor11b(conditionsList) -> bool:
    conditions = makeConditionsFromSigmas(conditionsList)
    foundCondition1 = False
    foundCondition2 = False
    if len(conditions) == 2:  # We need to have exactly two conditions in this sigma
        for condition in conditions:
            if condition == "R.D=S.D" or condition == "S.D=R.D":
                foundCondition1 = True
            elif condition == "R.E=S.E" or condition == "S.E=R.E":
                foundCondition2 = True
            if foundCondition1 and foundCondition2:
                return True
        return False
    return False


def canExecuteRule11b(algebricExpression) -> bool:
    for i in range(len(algebricExpression)):
        if type(algebricExpression[i]) is Sigma:
            if i + 1 < len(algebricExpression):
                if type(algebricExpression[i + 1]) is Cartesian:
                    if isTheRightConditionFor11b(algebricExpression[i].conditionsList):
                        # We are taking out the sigma with the condition, it is no longer needed
                        algebricExpression.pop(i) 
                        return True

    return False


def rule4(algebricExpression) -> None:
    for item in algebricExpression:
        if type(item) is Sigma:
            index = 0
            for condition in item.conditionsList:
                if "AND" in condition:
                    splitedSigmas = splitSigmaByAND(condition)
                    item.conditionsList.pop(index)
                    item.conditionsList.insert(index, splitedSigmas[0])
                    item.conditionsList.insert(index + 1, splitedSigmas[1])
                    return
                index += 1
    return


def rule4a(algebricExpression) -> None:
    for item in algebricExpression:
        if type(item) is Sigma:
            #If we have two different conditions in a sigma condition list meaning it is a sigma inside a sigma
            if len(item.conditionsList) > 1: 
                #We swap the conditions, meaning we swaped the order of who within who
                item.conditionsList[0], item.conditionsList[1] = item.conditionsList[1], item.conditionsList[0]
                return

def isOnlyRCondition(condition, tableR, tableS) -> bool:
    #This function check if there is only R related conditions in the string
    condition = cleanCondition(condition)
    leftIndex = 0
    rightIndex = 1

    while leftIndex < len(condition.split(",")):
        firstBlock = condition.split(",")[leftIndex]
        secondBlock = condition.split(",")[rightIndex]
        if firstBlock not in tableR or secondBlock in tableS:
            return False
        leftIndex += 2
        rightIndex += 2
    return True


def isOnlySCondition(condition, tableR, tableS) -> bool:
    #This function check if there is only S related conditions in the string
    condition = cleanCondition(condition)
    leftIndex = 0
    rightIndex = 1

    while leftIndex < len(condition.split(",")):
        firstBlock = condition.split(",")[leftIndex]
        secondBlock = condition.split(",")[rightIndex]
        if firstBlock not in tableS or secondBlock in tableR:
            return False
        leftIndex += 2
        rightIndex += 2
    return True


def rule5a(algebricExpression) -> None:
    for i in range(len(algebricExpression)):
        if type(algebricExpression[i]) is PI:
            if type(algebricExpression[i + 1]) is Sigma:
                algebricExpression[i], algebricExpression[i + 1] = algebricExpression[i + 1], algebricExpression[i]


def rule6(algebricExpression, tableR, tableS) -> None:
    sigmaR = Sigma()
    sigmaS = Sigma()
    sigmaRS = Sigma()
    for item in algebricExpression:
        if type(item) is Sigma:
            for condition in item.conditionsList:
                if isOnlyRCondition(condition, tableR, tableS):
                    sigmaR.conditionsList.append(condition)
                elif isOnlySCondition(condition, tableR, tableS):
                    sigmaS.conditionsList.append(condition)
                else:
                    sigmaRS.conditionsList.append(condition)
            item.conditionsList = sigmaRS.conditionsList
    for item in algebricExpression:
        if type(item) is Sigma:
            if not item.conditionsList:
                algebricExpression.remove(item)

    for item in algebricExpression:
        if type(item) is Cartesian:
            if "R" in item.firstTable:
                if sigmaR.conditionsList:
                    item.firstTable[0] = sigmaR
                    item.firstTable.append("(R)")
            else:
                if sigmaS.conditionsList:
                    item.firstTable[0] = sigmaS
                    item.firstTable.append("(S)")
            if "R" in item.secondTable:
                if sigmaR.conditionsList:
                    item.secondTable[0] = sigmaR
                    item.secondTable.append("(R)")
            else:
                if sigmaS.conditionsList:
                    item.secondTable[0] = sigmaS
                    item.secondTable.append("(S)")


def rule11b(algebricExpression) -> None:
    for item in algebricExpression:
        if type(item) is Cartesian:
            item.isNjoin = True
            item.name = "Njoin"

def runRulesRandomly(algebricExpression, tableR, tableS):
    queries = [copy.deepcopy(algebricExpression),copy.deepcopy(algebricExpression),
               copy.deepcopy(algebricExpression),copy.deepcopy(algebricExpression)]
    for j in range(0,4): #We run 4 rounds in order to calculate 4 different queries
        print("=================")
        print("Logical query #" + str(j+1))
        print("=================", end="\n\n")
        for i in range(10): #For each query we raffle 10 rules to execute on the query
            print("Round #" + str(i+1))
            print("-----------", end="\n")
            number = random.randint(1, 6)
            if number == 1:
                if canExecuteRule4(queries[j]):
                    rule4(queries[j])
                    print("Query after executing rule 4:")
                else:
                    print("Can't execute rule 4, Logical query didn't change")
            elif number == 2:
                if canExecuteRule4a(queries[j]):
                    rule4a(queries[j])
                    print("Query after executing rule 4a:")
                else:
                    print("Can't execute rule 4a, Logical query didn't change")
            elif number == 3:
                if canExecuteRule5a(queries[j], tableR, tableS):
                    rule5a(queries[j])
                    print("Query after executing rule 5a:")
                else:
                    print("Can't execute rule 5a, Logical query didn't change")
            elif number == 4:
                if canExecuteRule6(queries[j], tableR, tableS):
                    rule6(queries[j],tableR,tableS)
                    print("Query after executing rule 6:")
                else:
                    print("Can't execute rule 6 Logical query didn't change")
            elif number == 5:
                if canExecuteRule6(queries[j], tableR, tableS):
                    rule6(queries[j],tableR,tableS)
                    print("Query after executing rule 6a:")
                else:
                    print("Can't execute rule 6a, Logical query didn't change")
            else:
                if canExecuteRule11b(queries[j]):
                    rule11b(queries[j])
                    print("Query after executing rule 11b:")
                else:
                    print("Can't execute rule 11b, Logical query didn't change")
            printAlgebricExpression(queries[j])
            print("\n")
        print("\n")
    return queries

def getDataFromFile():
    #We scan for the data from the statistics file
    data = { 
        'R': {'n_R': int, 'R_R': int, 'V(A)': int, 'V(B)': int, 'V(C)': int, 'V(D)': int, 'V(E)': int},
        'S': {'n_S': int, 'R_S': int, 'V(D)': int, 'V(E)': int, 'V(F)': int, 'V(H)': int, 'V(I)': int}
    }

    file = open("statistics.txt", 'r')

    for line in file:
        if line == "Scheme R\n":
            table = "R"
        elif line == "Scheme S\n":
            table = "S"
        elif line.count("INTEGER") > 0:
            if table == "S":
                data.get(table)["R_S"] = 4 * line.count("INTEGER")
            else:
                data.get(table)["R_R"] = 4 * line.count("INTEGER")
        elif line == "\n":
            continue
        else:
            line = line[:-1]
            keyAndData = line.split("=")
            data.get(table)[keyAndData[0]] = int(keyAndData[1])

    file.close()
    return data

def piCalculator(lastArg, sum2, data):
    retSum = {'n_Scheme': sum2['n_Scheme'], 'R_Scheme': int}
    retSum['R_Scheme'] = len(lastArg.attributesList)*4

    return retSum


def calculateSimpleCondition(condition, data):
    index = condition.find("=")
    firstProb = 0
    if index != -1:
        firstArg = condition[:index]
        secondArg = condition[index + 1:]
        indexOfPoint = firstArg.find(".")
        if indexOfPoint != -1:
            listOfStrings = firstArg.split('.')
            first1 = listOfStrings[0]
            second1 = listOfStrings[1]
            second1 = "V(" + second1 + ")"
            numOfDifferentValues1 = data.get(first1).get(second1)
            firstProb = 1.0 / numOfDifferentValues1

        indexOfPoint = secondArg.find(".")
        if indexOfPoint != -1:
            listOfStrings = firstArg.split('.')
            first2 = listOfStrings[0]
            second2 = listOfStrings[1]
            second2 = "V(" + second2 + ")"
            numOfDifferentValues2 = data.get(first2).get(second2)
            secondProb = 1.0 / numOfDifferentValues2
            if numOfDifferentValues1 > numOfDifferentValues2:
                return firstProb
            else:
                return secondProb
        else:
            return firstProb

def calculateConditions(sigma, data):
    conditions = makeConditionsFromSigmas(sigma)
    conditions[0] = conditions[0].replace("(","")
    conditions[0] = conditions[0].replace(")","")
    res = calculateSimpleCondition(conditions[0],data)
    for condition in conditions[1:]:
        condition = condition.replace("(", "")
        condition = condition.replace(")", "")
        res *= calculateSimpleCondition(condition,data)
    return res


def sigmaCalculator(sigma, sum1, data):
    result = calculateConditions(sigma, data)
    return int(result * sum1)


def cartesianCalculator(cartesian, data):
    sumToReturn = {'n_Scheme': None, 'R_Scheme': None}
    res1 = -1
    res2 = -1

    if isinstance(cartesian.firstTable[0], Sigma):
        if "R" in cartesian.firstTable:
            res1 = sigmaCalculator(cartesian.firstTable[0].conditionsList, data.get("R")["n_R"], data)
        else:
            res1 = sigmaCalculator(cartesian.firstTable[0].conditionsList, data.get("S")["n_S"], data)
    if isinstance(cartesian.secondTable[0], Sigma):
        if "R" in cartesian.secondTable:
            res2 = sigmaCalculator(cartesian.secondTable[0].conditionsList, data.get("R")["n_R"], data)
        else:
            res2 = sigmaCalculator(cartesian.secondTable[0].conditionsList, data.get("S")["n_S"], data)
    if res1 != -1:
        if res2 != -1:  # In this case there are two sigmas in the cartesian
            sumToReturn['n_Scheme'] = res1 * res2
            sumToReturn['R_Scheme'] = data.get('R').get('R_R') + data.get('S').get('R_S')
            return sumToReturn
        else:  #  In this case only the left argument is sigma
            if cartesian.secondTable == "S":
                sumToReturn['n_Scheme'] = res1 * data.get('S').get('n_S')
                sumToReturn['R_Scheme'] = data.get('R').get('R_R') + data.get('S').get('R_S')
                return sumToReturn
            else:
                sumToReturn['n_Scheme'] = res1 * data.get('R').get('n_R')
                sumToReturn['R_Scheme'] = data.get('R').get('R_R') + data.get('S').get('R_S')
                return sumToReturn
    elif res1 == -1:
        if res2 != -1: # In this case only right argument is sigma
            if cartesian.firstTable[0] == "S":
                sumToReturn['n_Scheme'] = res2 * data.get('S').get('n_S')
                sumToReturn['R_Scheme'] = data.get('R').get('R_R') + data.get('S').get('R_S')
                return sumToReturn
            else:
                sumToReturn['n_Scheme'] = res2 * data.get('R').get('n_R')
                sumToReturn['R_Scheme'] = data.get('R').get('R_R') + data.get('S').get('R_S')
                return sumToReturn
        else:  # In this case both arguments are the original table
            sumOfArgument = data.get('R').get('n_R') * data.get('S').get('n_S')
            sumToReturn['n_Scheme'] = sumOfArgument
            sumToReturn['R_Scheme'] = data.get('R').get('R_R') + data.get('S').get('R_S')
            return sumToReturn


def NjoinCalculator(nJoin, data):
    result1 = -1
    result2 = -1
    sumToReturn = {'n_Scheme': int, 'R_Scheme': int}
    tableSize = data.get("R")['n_R'] * data.get("S")['n_S']
    if data.get("R")['V(D)'] > data.get("S")['V(D)']:
        Vd = 1/data.get("R")['V(D)']
    else:
        Vd = 1/data.get("S")['V(D)']
    if data.get("R")['V(E)'] > data.get("S")['V(E)']:
        Ve = 1/data.get("R")['V(E)']
    else:
        Ve = 1/data.get("S")['V(E)']

    if isinstance(nJoin.firstTable[0], Sigma):
        if "R" in nJoin.firstTable:
            result1 = sigmaCalculator(nJoin.firstTable[0].conditionsList, data.get("R")["n_R"], data)
        else:
            result1 = sigmaCalculator(nJoin.firstTable[0].conditionsList, data.get("S")["n_S"], data)
    if isinstance(nJoin.secondTable[0], Sigma):
        if "R" in nJoin.secondTable:
            result2 = sigmaCalculator(nJoin.secondTable[0].conditionsList, data.get("R")["n_R"], data)
        else:
            result2 = sigmaCalculator(nJoin.secondTable[0].conditionsList, data.get("S")["n_S"], data)
    if result1 != -1:
        if result2 != -1:  # In this case there are two sigmas in the cartesian
            sumToReturn['n_Scheme'] = int((1/result1 * 1/result2) * tableSize)
            sumToReturn['R_Scheme'] = int(data.get('R').get('R_R') + data.get('S').get('R_S'))
            return sumToReturn
        else: #  In this case only the left argument is sigma
                sumToReturn['n_Scheme'] = int(1/result1 * Vd * Ve * tableSize)
                sumToReturn['R_Scheme'] = int(data.get('R').get('R_R') + data.get('S').get('R_S'))
                return sumToReturn
    elif result1 == -1:
        if result2 != -1: # In this case only right argument is sigma
                sumToReturn['n_Scheme'] = int(1/result2 * Vd * Ve * tableSize)
                sumToReturn['R_Scheme'] = int(data.get('R').get('R_R') + data.get('S').get('R_S'))
                return sumToReturn
        else:  # In this case two arguments are the original table
            sumToReturn['n_Scheme'] = int(Vd * Ve * tableSize)
            sumToReturn['R_Scheme'] = int(data.get('R').get('R_R') + data.get('S').get('R_S'))
            return sumToReturn


def printPiSum(lastArg, iSum, oSum):
    print(lastArg.name)
    print("\tInput: n_Scheme = " + str(iSum['n_Scheme']) + ' R_Scheme = ' + str(iSum['R_Scheme']))
    print("\tOutput: n_Scheme = " + str(oSum['n_Scheme']) + ' R_Scheme = ' + str(oSum['R_Scheme']))

def printSigmaSum(lastArg, iSum, oSum):
    print(lastArg.name)
    print("\tInput: n_Scheme = " + str(iSum['n_Scheme']) + ' R_Scheme = ' + str(iSum['R_Scheme']))
    print("\tOutput: n_Scheme = " + str(oSum['n_Scheme']) + ' R_Scheme = ' + str(oSum['R_Scheme']))

def printCartesianSum(sum, argument, data):
    print(argument.name)
    print(
        "\tInput: n_R = " + str(data.get("R")["n_R"]) + ", n_S =" + str(data.get("S")["n_S"]) + ", R_R = " + str(data.get("R")["R_R"])
        + ", R_S = " + str(data.get("S")["R_S"]))
    print("\tOutput: n_Scheme = " + str(sum['n_Scheme']) + ' R_Scheme = ' + str(sum['R_Scheme']))


def CalculateQuery(queriesList):
    data = getDataFromFile()
    sum1 = {'n_Scheme': None, 'R_Scheme': None}
    sum2 = {'n_Scheme': None, 'R_Scheme': None}
    sum3 = {'n_Scheme': None, 'R_Scheme': None}

    while len(queriesList) != 0:
        query = queriesList.pop()
        while len(query) != 0:
            lastArg = query.pop()
            if isinstance(lastArg, Cartesian):
                if(not lastArg.isNjoin):
                    sum1 = cartesianCalculator(lastArg, data)
                    if sum1["n_Scheme"] is not None:
                        printCartesianSum(sum1, lastArg, data)
                else:
                    sum1 = NjoinCalculator(lastArg, data)
                    if sum1["n_Scheme"] is not None:
                        printCartesianSum(sum1, lastArg, data)
            elif isinstance(lastArg, Sigma):
                if sum1["n_Scheme"] is not None:
                    sum2["n_Scheme"] = sigmaCalculator(lastArg.conditionsList, sum1["n_Scheme"], data)
                    sum2["R_Scheme"] = sum1["R_Scheme"]
                    printSigmaSum(lastArg, sum1, sum2)
            else:
                if sum2["n_Scheme"] is not None:
                    sum3 = piCalculator(lastArg, sum2, data)
                    printPiSum(lastArg, sum2, sum3)
                else:
                    sum3 = piCalculator(lastArg, sum1, data)
                    printPiSum(lastArg, sum1, sum3)

        print("------------------------------------")

def printAlgebricExpressionItem(item) -> None:
    if type(item) is PI:
        print("PI[", end="")
        for element in item.attributesList[0:-1]:
            print(element.strip(" ") + ",", end="")
        print(item.attributesList[-1].strip() + "]" + "(", end="")
    elif type(item) is Sigma:
        print("SIGMA[", end="")
        print(item.conditionsList[0].strip() + "]" + "(", end="")
        for element in item.conditionsList[1:-1]:
            print("SIGMA[", end="")
            print(element.strip() + "]" + "(", end="")
        if len(item.conditionsList) > 1:
            print("SIGMA[", end="")
            print(item.conditionsList[-1].strip() + "]" + "(", end="")
    elif type(item) is str:
        print(item.strip(), end="")


def printAlgebricExpression(algebricExpression) -> None:
    for item in algebricExpression:
        if type(item) is Cartesian:
            if (item.isNjoin):
                print("NJOIN(", end="")
            else:
                print("CARTESIAN(", end="")
            for cartesianItem in item.firstTable:
                printAlgebricExpressionItem(cartesianItem)
            print(",", end="")
            for cartesianItem in item.secondTable:
                printAlgebricExpressionItem(cartesianItem)
        else:
            printAlgebricExpressionItem(item)
    print(")" * len(algebricExpression))


def test(algebricExpression, tableR, tableS) -> None:
    queries = [copy.deepcopy(algebricExpression),copy.deepcopy(algebricExpression),
               copy.deepcopy(algebricExpression),copy.deepcopy(algebricExpression)]
    for j in range(0,4): #We run 4 rounds in order to calculate 4 different queries
        print("=================")
        print("Logical query #" + str(j+1))
        print("=================", end="\n\n")
        for i in range(10): #For each query we raffle 10 rules to execute on the query
            print("Round #" + str(i+1))
            print("-----------", end="\n")
            number = i%6
            if number == 1:
                if canExecuteRule4(queries[j]):
                    rule4(queries[j])
                    print("Query after executing rule 4:")
                else:
                    print("Can't execute rule 4, Logical query didn't change")
            elif number == 2:
                if canExecuteRule4a(queries[j]):
                    rule4a(queries[j])
                    print("Query after executing rule 4a:")
                else:
                    print("Can't execute rule 4a, Logical query didn't change")
            elif number == 3:
                if canExecuteRule5a(queries[j], tableR, tableS):
                    rule5a(queries[j])
                    print("Query after executing rule 5a:")
                else:
                    print("Can't execute rule 5a, Logical query didn't change")
            elif number == 4:
                if canExecuteRule6(queries[j], tableR, tableS):
                    rule6(queries[j],tableR,tableS)
                    print("Query after executing rule 6:")
                else:
                    print("Can't execute rule 6 Logical query didn't change")
            elif number == 5:
                if canExecuteRule6(queries[j], tableR, tableS):
                    rule6(queries[j],tableR,tableS)
                    print("Query after executing rule 6a:")
                else:
                    print("Can't execute rule 6a, Logical query didn't change")
            else:
                if canExecuteRule11b(queries[j]):
                    rule11b(queries[j])
                    print("Query after executing rule 11b:")
                else:
                    print("Can't execute rule 11b, Logical query didn't change")
            printAlgebricExpression(queries[j])
            print("\n")
        print("\n")
    return queries

def __main__():

    #We keep all of our possible columns
    tableR = ["R.A", "R.B", "R.C", "R.D", "R.E"]
    tableS = ["S.E", "S.F", "S.G", "S.D", "S.I"]

    #Get query from user
    sqlQuery = input("Please enter the SQL query")
    sqlQuery = sqlQuery.strip(" ")

    if sqlQuery[-1] == ";": 
        sqlQuery = sqlQuery[0:-1]

    select = sqlQuery.partition(" ")[0]
    select = select.upper()
    sqlQuery = cleanString(sqlQuery, select)

    piBlock = sqlQuery.split("FROM")[0].strip()
    sqlQuery = cleanString(sqlQuery, piBlock)
    cartesianBlock = sqlQuery.split("WHERE")[0].split("FROM")[1].strip()
    sqlQuery = cleanString(sqlQuery, cartesianBlock).split("WHERE")[1]
    sigmaBlock = sqlQuery.strip()

    # We save all of our query parts in data stractures
    Sigmas = Sigma()
    Sigmas.conditionsList.append(sigmaBlock)

    piBlock = piBlock.replace(" ", "")
    Pis = PI()
    Pis.attributesList = str(piBlock).split(",")

    Cartesians = Cartesian()
    if not "," in cartesianBlock:
        Cartesians.firstTable.append(cartesianBlock)
        Cartesians.secondTable.append(cartesianBlock)
    else:
        Cartesians.firstTable.append(cartesianBlock.split(",")[0].strip())
        Cartesians.secondTable.append(cartesianBlock.split(",")[1].strip())

    #We build the algebric expression in a list
    algebricExpression = []
    algebricExpression.append(Pis)
    algebricExpression.append(Sigmas)
    algebricExpression.append(Cartesians)
    algebricExpression[1] = clearBrackets(algebricExpression[1])

    printAlgebricExpression(algebricExpression)
    print("---------------------")
    #We make 4 different logical queries using random rules and keep them all in a quries list
    queries = runRulesRandomly(algebricExpression, tableR, tableS)

    #We calculate each query
    CalculateQuery(queries)



__main__()



