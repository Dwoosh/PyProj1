import string
import itertools

#checks if expression is correct
def checkExpression(expression):
    expression = expression.replace(" ","")
    brackets = 0
    firstStep = True
    operators = ['∧', '∨', '^', '⇒', '⇔']
    negation = '¬'
    for letter in expression:
        if firstStep:
            if letter == '(':
                brackets += 1
            elif letter.isalpha():
                firstStep = False
            elif letter is negation:
                pass
            else: return False
        else:
            if letter == ')':
                brackets -= 1
                if brackets < 0: return False
            elif letter in operators:
                firstStep = True
            else: return False
    return brackets == 0 and not firstStep

#returns list of letters in expression
def getListOfLetters(expression):
    return [e for e in string.ascii_lowercase if e in expression]

#returns amount of letters in expression
def getNumberOfLetters(expression):
    l = getListOfLetters(expression)
    return len(l)

#calculates given operation
def calculate(item1,item2,operator):
    if operator == '¬':
        if item2 == '1':
            item2 = '0'
        else:
            item2 = '1'
        return item2

    elif operator == '∧':
        if item1 == '1' and item2 == '1':
            return '1'
        else:
            return '0'

    elif operator == '∨':
        if item1 == '0' and item2 == '0':
            return '0'
        else:
            return '1'

    elif operator == '^':
        if item1 == item2:
            return '0'
        else:
            return '1'

    elif operator == '⇔':
        if item1 == item2:
            return '1'
        else:
            return '0'

    elif operator == '⇒':
        if item1 == '1' and item2 == '0':
            return '0'
        else:
            return '1'

#evaluates expression for given values of letters
def evaluateExpression(expr,letters,values):
    #change letters to their values
    index = 0
    for item in expr:
        if item in letters:
            place = letters.index(item)
            expr = expr[:index] + values[place] + expr[index+1:]
        index += 1
    #convert to reverse polish notation
    operators = ['∧', '∨', '^', '⇒', '⇔', '¬']
    priority = {'(': 0, ')': 1, '∧': 2, '∨': 1, '^': 3, '⇒': 1, '⇔': 1, '¬': 4}
    stack = []
    result = []
    for item in expr:
        if item in operators:
            while stack and priority[stack[-1]] >= priority[item]:
                result.append(stack.pop())
            stack.append(item)
        elif item is '(':
            stack.append(item)
        elif item is ')':
            while stack and stack[-1] is not '(':
                result.append(stack.pop())
            stack.pop() #pops left bracket
        else:
            result.append(item)
    while len(stack) is not 0:
        result.append(stack.pop())
    #calculate expression
    stack = []
    while result:
        if result[0] not in operators:
            stack.append(result.pop(0))
        else:
            if result[0] is '¬':
                stack.append(calculate('',stack.pop(),result.pop(0)))
            else:
                stack.append(calculate(stack.pop(),stack.pop(),result.pop(0)))
    return stack[0]

#turns number to binary representation with leading zeros
def turnToBinary(number,length):
    binary = str(bin(number))[2:]
    while len(binary) != length:
        binary = '0' + binary
    return binary

#returns true if string contains given number of 1
def hasNumberOfOnes(binary, number):
    ones = 0
    for c in binary:
        if c is '1':
            ones += 1
    return ones == number

#checks if strings vary only by one character
#and returns simplified string if it can
def getSimpleString(binary1,binary2):
    diffByOne = False
    simpleStr = ''
    for i in range(0,len(binary1)):
        if binary1 != binary2:
            if binary1 != '-' and binary2 != '-' and not diffByOne:
                simpleStr = simpleStr + '-'
                diffByOne = True
            else: return ''
        else: simpleStr = simpleStr + binary1[i]
    return simpleStr

#returns false if string cant be represented by any of the items in list
def canBeRepresented(binary,impl):
    can = True
    length = len(binary)
    for item in impl:
        for i in range(0,length):
            if impl[i] != '-' and impl[i] != binary[i]:
                can = False
    return can

def main():
    st = "¬(a∧b)⇔(a⇒c)"
    if checkExpression(st) is False:
        print("Expression has wrong syntax")
        return 1
    variables = sorted(getListOfLetters(st))
    count = getNumberOfLetters(st)
    table = {}
    for i in range(0,2**count):
        binary = turnToBinary(i,count)
        table[binary] = evaluateExpression(st,variables,list(binary))
    #check if expression is tautology and remove values other than 1
    isTautology = True
    toDelete = []
    for k, v in table.items():
        if v is '0':
            isTautology = False
            toDelete.append(k)
    if isTautology is True:
        print("Given expression is tautology")
        return 0
    for key in toDelete:
        del table[key]
    #checks for higher size implicants
    noMore = False
    resultChart = []
    implicants = []
    higherImpl = []
    for k, v in table.items():
            implicants.append(k)
    while not noMore:
        if not higherImpl:
            implicants = higherImpl
            higherImpl = []
    #check for higher size implicants
        if len(implicants) == 1:
            resultChart.append(implicants[0])
            break
        for pair in itertools.combinations(implicants,2):
            simpler = getSimpleString(pair[0],pair[1])
            if simpler is not '':
                higherImpl.append(simpler)
    #if there are no higher size implicants
        if not higherImpl:
            resultChart = implicants
            noMore = True
        else:
            for item in implicants:
                if not canBeRepresented(item,higherImpl):
                    resultChart.append(item)
    #-pobieram binary i zwracam liste mozliwych stringow
    #-probuje dobrac kazdy string do kazdego binary, jesli moze byc
    #representowany tylko przez jeden binary to dodaje binary do wyniku
    #-konwertuje wynikowe binary na ciagi znakow


    
    
if __name__ == '__main__':
    main()
    
