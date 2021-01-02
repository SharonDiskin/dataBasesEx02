###

import copy
import random


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


def checkIfMainAnd(firstSigma, secondSigma) -> bool:
    return str(firstSigma).count("(") == str(firstSigma).count(")") and \
           str(secondSigma).count(")") == str(secondSigma).count("(")


def deleteBracket(sigma) -> str:
    sigma = str(sigma).strip()
    index = -1;
    while (str(sigma).count(")") > str(sigma).count("(")):
        if (sigma[index] == ")"):
            if (index == -1):
                sigma = sigma[:index]
            else:
                sigma = sigma[:index] + sigma[index + 1:]
        else:
            index -= 1
    index = 0
    while (str(sigma).count(")") < str(sigma).count("(")):
        if sigma[index] == "(":
            sigma = sigma[:index] + sigma[index + 1:]
        else:
            index += 1
    while (sigma[0] == "(" and sigma[-1] == ")"):
        sigma = sigma[1:-1]
        sigma = sigma.strip()
    return sigma


def splitSigmaByAND(sigma) -> list:
    tempStr = sigma
    index = 0
    while ("AND" in tempStr):
        index += str(tempStr).find("AND")
        if (checkIfMainAnd(sigma[0:index], sigma[index + 3:])):
            sigmas = [deleteBracket(sigma[0:index]), deleteBracket(sigma[index + 3:])]
            return sigmas
        else:
            index += 3
            tempStr = tempStr[index:]
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
    # We lay on the assumption that is the sigma block contains at least one "AND" we can use rule 4
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
            if len(item.conditionsList) > 1:
                item.conditionsList[0], item.conditionsList[1] = item.conditionsList[1], item.conditionsList[0]
                return


def isOnlyRCondition(condition, tableR, tableS) -> bool:
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


def runRulesRandomly(algebricExpression, tableR, tableS):
    queries = [copy.deepcopy(algebricExpression),copy.deepcopy(algebricExpression),
               copy.deepcopy(algebricExpression),copy.deepcopy(algebricExpression)]
    for j in range(0,4):
        print("=================")
        print("Logical query #" + str(j+1))
        print("=================", end="\n\n")
        for i in range(10):
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

def GetDataFromFile():
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

def CalculateCartesian(cartesian, data):
    sumToReturn = {'n_Scheme': None, 'R_Scheme': None}
    result1 = -1
    result2 = -1

    if isinstance(cartesian.firstTable[0], Sigma):
        if "R" in cartesian.firstTable:
            result1 = CalculateSigma(cartesian.firstTable[0].conditionsList, data.get("R")["n_R"], data)
        else:
            result1 = CalculateSigma(cartesian.firstTable[0].conditionsList, data.get("S")["n_S"], data)
    if isinstance(cartesian.secondTable[0], Sigma):
        if "R" in cartesian.secondTable:
            result2 = CalculateSigma(cartesian.secondTable[0].conditionsList, data.get("R")["n_R"], data)
        else:
            result2 = CalculateSigma(cartesian.secondTable[0].conditionsList, data.get("S")["n_S"], data)
    if result1 != -1:
        if result2 != -1:
            # two sigmas in the cartesian
            sumToReturn['n_Scheme'] = result1 * result2
            sumToReturn['R_Scheme'] = data.get('R').get('R_R') + data.get('S').get('R_S')
            return sumToReturn
        # only the left argument is sigma
        else:
            if cartesian.secondTable == "S":
                sumToReturn['n_Scheme'] = result1 * data.get('S').get('n_S')
                sumToReturn['R_Scheme'] = data.get('R').get('R_R') + data.get('S').get('R_S')
                return sumToReturn
            else:
                sumToReturn['n_Scheme'] = result1 * data.get('R').get('n_R')
                sumToReturn['R_Scheme'] = data.get('R').get('R_R') + data.get('S').get('R_S')
                return sumToReturn
    elif result1 == -1:
        if result2 != -1:
            # only right argument is sigma
            if cartesian.firstTable[0] == "S":
                sumToReturn['n_Scheme'] = result2 * data.get('S').get('n_S')
                sumToReturn['R_Scheme'] = data.get('R').get('R_R') + data.get('S').get('R_S')
                return sumToReturn
            else:
                sumToReturn['n_Scheme'] = result2 * data.get('R').get('n_R')
                sumToReturn['R_Scheme'] = data.get('R').get('R_R') + data.get('S').get('R_S')
                return sumToReturn
        else:
            # two arguments are the original table
            sumOfArgument = data.get('R').get('n_R') * data.get('S').get('n_S')
            sumToReturn['n_Scheme'] = sumOfArgument
            sumToReturn['R_Scheme'] = data.get('R').get('R_R') + data.get('S').get('R_S')
            return sumToReturn


def CalculateNjoin(nJoin, data):
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
            result1 = CalculateSigma(nJoin.firstTable[0].conditionsList, data.get("R")["n_R"], data)
        else:
            result1 = CalculateSigma(nJoin.firstTable[0].conditionsList, data.get("S")["n_S"], data)
    if isinstance(nJoin.secondTable[0], Sigma):
        if "R" in nJoin.secondTable:
            result2 = CalculateSigma(nJoin.secondTable[0].conditionsList, data.get("R")["n_R"], data)
        else:
            result2 = CalculateSigma(nJoin.secondTable[0].conditionsList, data.get("S")["n_S"], data)
    if result1 != -1:
        if result2 != -1:
            # two sigmas in the cartesian
            sumToReturn['n_Scheme'] = int((1/result1 * 1/result2) * tableSize)
            sumToReturn['R_Scheme'] = int(data.get('R').get('R_R') + data.get('S').get('R_S'))
            return sumToReturn
        # only the left argument is sigma
        else:
                sumToReturn['n_Scheme'] = int(1/result1 * Vd * Ve * tableSize)
                sumToReturn['R_Scheme'] = int(data.get('R').get('R_R') + data.get('S').get('R_S'))
                return sumToReturn
    elif result1 == -1:
        if result2 != -1:
            # only right argument is sigma
                sumToReturn['n_Scheme'] = int(1/result2 * Vd * Ve * tableSize)
                sumToReturn['R_Scheme'] = int(data.get('R').get('R_R') + data.get('S').get('R_S'))
                return sumToReturn
        else:
            # two arguments are the original table
            sumToReturn['n_Scheme'] = int(Vd * Ve * tableSize)
            sumToReturn['R_Scheme'] = int(data.get('R').get('R_R') + data.get('S').get('R_S'))
            return sumToReturn

def CalculateSigmaConditions(sigma, data):
    conditions = makeConditionsFromSigmas(sigma)
    conditions[0] = conditions[0].replace("(","")
    conditions[0] = conditions[0].replace(")","")
    result = CalculateSimpleCondition(conditions[0],data)
    for condition in conditions[1:]:
        condition = condition.replace("(", "")
        condition = condition.replace(")", "")
        result *= CalculateSimpleCondition(condition,data)
    return result

def CalculateSigma(sigma, sum1, data):
    result = CalculateSigmaConditions(sigma, data)
    return int(result * sum1)


def CalculatePi(lastArg, sum2, data):
    sumToReturn = {'n_Scheme': sum2['n_Scheme'], 'R_Scheme': int}

    sumToReturn['R_Scheme'] = 4* len(lastArg.attributesList)

    return sumToReturn


def PrintSumOfQueryCartesian(sumToPrint, argumentToPrint, data):
    print(argumentToPrint.name)
    print(
        "\tInput: n_R = " + str(data.get("R")["n_R"]) + ", n_S =" + str(data.get("S")["n_S"]) + ", R_R = " + str(data.get("R")["R_R"])
        + ", R_S = " + str(data.get("S")["R_S"]))
    print("\tOutput: n_Scheme = " + str(sumToPrint['n_Scheme']) + ' R_Scheme = ' + str(sumToPrint['R_Scheme']))


def PrintSumOfQuerySigma(lastArg, sumInput, sumOutput):
    print(lastArg.name)
    print("\tInput: n_Scheme = " + str(sumInput['n_Scheme']) + ' R_Scheme = ' + str(sumInput['R_Scheme']))
    print("\tOutput: n_Scheme = " + str(sumOutput['n_Scheme']) + ' R_Scheme = ' + str(sumOutput['R_Scheme']))

def PrintSumOfQueryPi(lastArg, sumInput, sumOutput):
    print(lastArg.name)
    print("\tInput: n_Scheme = " + str(sumInput['n_Scheme']) + ' R_Scheme = ' + str(sumInput['R_Scheme']))
    print("\tOutput: n_Scheme = " + str(sumOutput['n_Scheme']) + ' R_Scheme = ' + str(sumOutput['R_Scheme']))

def CalculateSimpleCondition(condition, data):
    index = condition.find("=")
    prob1 = 0
    if index != -1:
        arg1 = condition[:index]
        arg2 = condition[index + 1:]
        indexOfPoint = arg1.find(".")
        if indexOfPoint != -1:
            listOfStrings = arg1.split('.')
            first1 = listOfStrings[0]
            second1 = listOfStrings[1]
            second1 = "V(" + second1 + ")"
            numberOfDifferentValues1 = data.get(first1).get(second1)
            prob1 = 1 / numberOfDifferentValues1

        indexOfPoint = arg2.find(".")
        if indexOfPoint != -1:
            listOfStrings = arg1.split('.')
            first2 = listOfStrings[0]
            second2 = listOfStrings[1]
            second2 = "V(" + second2 + ")"
            numberOfDifferentValues2 = data.get(first2).get(second2)
            prob2 = 1 / numberOfDifferentValues2
            if numberOfDifferentValues1 > numberOfDifferentValues2:
                return prob1
            else:
                return prob2
        else:
            return prob1

def CalculateQuery(queriesList):
    data = GetDataFromFile()
    #########################

    sum1 = {'n_Scheme': None, 'R_Scheme': None}
    sum2 = {'n_Scheme': None, 'R_Scheme': None}
    sum3 = {'n_Scheme': None, 'R_Scheme': None}
    while len(queriesList) != 0:
        query = queriesList.pop()
        while len(query) != 0:
            lastArg = query.pop()
            if isinstance(lastArg, Cartesian):
                if(not lastArg.isNjoin):
                    sum1 = CalculateCartesian(lastArg, data)
                    if sum1["n_Scheme"] is not None:
                        PrintSumOfQueryCartesian(sum1, lastArg, data)
                else:
                    sum1 = CalculateNjoin(lastArg, data)
                    if sum1["n_Scheme"] is not None:
                        PrintSumOfQueryCartesian(sum1, lastArg, data)
            elif isinstance(lastArg, Sigma):
                if sum1["n_Scheme"] is not None:
                    sum2["n_Scheme"] = CalculateSigma(lastArg.conditionsList, sum1["n_Scheme"], data)
                    sum2["R_Scheme"] = sum1["R_Scheme"]
                    PrintSumOfQuerySigma(lastArg, sum1, sum2)
            else:
                if sum2["n_Scheme"] is not None:
                    sum3 = CalculatePi(lastArg, sum2, data)
                    PrintSumOfQueryPi(lastArg, sum2, sum3)
                else:
                    sum3 = CalculatePi(lastArg, sum1, data)
                    PrintSumOfQueryPi(lastArg, sum1, sum3)

        print("------------------------------------")

def __main__():
    tableR = ["R.A", "R.B", "R.C", "R.D", "R.E"]
    tableS = ["S.E", "S.F", "S.G", "S.D", "S.I"]
    selectionOptions = ["4", "4a", "5a", "6", "6a", "11b"]

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

    algebricExpression = []
    algebricExpression.append(Pis)
    algebricExpression.append(Sigmas)
    algebricExpression.append(Cartesians)

    queries = runRulesRandomly(algebricExpression, tableR, tableS)
    printAlgebricExpression(queries[0])
    printAlgebricExpression(queries[1])
    printAlgebricExpression(queries[2])
    printAlgebricExpression(queries[3])
    CalculateQuery(queries)


__main__()



