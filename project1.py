import string
import itertools

#checks if expression is correct
def check_expression(expression):
    brackets = 0
    firstStep = True
    operators = ['*', '+', '^', '>', '=']
    negation = '!'
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
def get_list_of_letters(expression):
    return [e for e in string.ascii_lowercase if e in expression]

#returns amount of letters in expression
def get_number_of_letters(expression):
    l = get_list_of_letters(expression)
    return len(l)

#calculates given operation
def calculate(item1,item2,operator):
    if operator == '!':
        if item2 == '1':
            item2 = '0'
        else:
            item2 = '1'
        return item2

    elif operator == '*':
        if item1 == '1' and item2 == '1':
            return '1'
        else:
            return '0'

    elif operator == '+':
        if item1 == '0' and item2 == '0':
            return '0'
        else:
            return '1'

    elif operator == '^':
        if item1 == item2:
            return '0'
        else:
            return '1'

    elif operator == '=':
        if item1 == item2:
            return '1'
        else:
            return '0'

    elif operator == '>':
        if item1 == '1' and item2 == '0':
            return '0'
        else:
            return '1'

#evaluates expression for given values of letters
def evaluate_expression(expr,letters,values):
    #change letters to their values
    index = 0
    for item in expr:
        if item in letters:
            place = letters.index(item)
            expr = expr[:index] + values[place] + expr[index+1:]
        index += 1
    #convert to reverse polish notation
    operators = ['*', '+', '^', '>', '=', '!']
    priority = {'(': 0, ')': 1, '+': 1, '>': 1, '=': 1, '*': 2, '^': 3, '!': 4}
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
            if result[0] is '!':
                stack.append(calculate('',stack.pop(),result.pop(0)))
            else:
                stack.append(calculate(stack.pop(),stack.pop(),result.pop(0)))
    return stack[0]

#turns number to binary representation with leading zeros
def turn_to_binary(number,length):
    binary = str(bin(number))[2:]
    while len(binary) != length:
        binary = '0' + binary
    return binary

#returns true if string contains given number of 1
def has_number_of_ones(binary, number):
    ones = 0
    for c in binary:
        if c is '1':
            ones += 1
    return ones == number

#checks if strings vary only by one character
#and returns simplified string if it can
def get_simple_string(binary1,binary2):
    diffByOne = False
    simpleStr = ''
    for i in range(0,len(binary1)):
        if binary1[i] != binary2[i]:
            if binary1[i] != '-' and binary2[i] != '-' and not diffByOne:
                simpleStr = simpleStr + '-'
                diffByOne = True
            else: return ''
        else: simpleStr = simpleStr + binary1[i]
    return simpleStr

#returns false if string cant be represented by any of the items in list
def can_be_represented(binary,impl):
    canList = []
    length = len(binary)
    for item in impl:
        can = True
        for i in range(0,length):
            if item[i] != '-' and item[i] != binary[i]:
                can = False
        canList.append(can)
    return True in canList

#specification of above for one value not list, returns true if binary represents value
def represents(binary,value):
    length = len(binary)
    for i in range(0,length):
        if binary[i] != '-' and binary[i] != value[i]:
            return False
    return True

#turns binary representation string to bool expression using variables
def turn_to_expr(binary,vars):
    st = ''
    length = len(binary)
    for i in range(0,length):
        if binary[i] is not '-':
            if st != '': st += '*'
            if binary[i] is '1':
                st += vars[i]
            else: st = st + '!' + vars[i]
        else:
            pass
    return st

#returns list of unique items from given list
def get_unique(lst):
    s = set(lst)
    return list(s)

def main():
    #prints information
    print("Use lowercase letters for variables")
    print("Use 1 or 0 for obvious true and false values")
    print("Use following symbols for operations:")
    print("* - AND, + - OR, ^ - XOR, > - IMPLIES, = - IFF, ! - NOT")
    print("Use brackets ( ) if necessary")
    print("! can be assigned to either variable or expression in brackets")
    print("AND and OR can be streamed (for example: a+b+c)")
    print("Use brackets for other operators (for example: (...)=(...)=(...))")
    print("Enter boolean expression you want to minimize:")
    st = input()
    #st = "!a*!b*!c*d+!a*b*!c*!d+!a*b*!c*d+!a*b*c*!d+a*!b*!c*d+a*!b*c*!d+a*!b*c*d+a*b*!c*d+a*b*c*!d"
    print("")
    st = st.replace(" ","")
    #checks if expression has correct syntax
    if check_expression(st) is False:
        print("Expression has wrong syntax")
        return 1
    #get list of variables and their amount
    variables = sorted(get_list_of_letters(st))
    count = get_number_of_letters(st)
    #creates dictionary and assigns to every possible binary combination
    #true or false to which given expression evaluates
    table = {}
    for i in range(0,2**count):
        binary = turn_to_binary(i,count)
        table[binary] = evaluate_expression(st,variables,list(binary))
    #check if expression is tautology and removes values other than 1
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
    #check for higher size implicants algorithm
    noMore = False
    implicantChart = []
    implicants = []
    higherImpl = []
    for k, v in table.items():
            implicants.append(k)
    while not noMore:
        if higherImpl:
            implicants = higherImpl
            higherImpl = []
        #check for higher size implicants
        if len(implicants) == 1:
            implicantChart.append(implicants[0])
            break
        for pair in itertools.combinations(implicants,2):
            simpler = get_simple_string(pair[0],pair[1])
            if simpler is not '':
                higherImpl.append(simpler)
        #if there are no higher size implicants
        if not higherImpl:
            implicantChart = implicants
            noMore = True
        else:
            for item in implicants:
                if not can_be_represented(item,higherImpl):
                    implicantChart.append(item)               
    #create list of values for which expression is true
    trueValues = []
    for k, v in table.items():
        trueValues.append(k)
    #solve chart
    chart = {}
    result = []
    for item in implicantChart:
        possibleValues = []
        for val in trueValues:
            if represents(item,val):
                possibleValues.append(val)
        chart[item] = possibleValues
    toDelete = []
    firstLoop = True
    while trueValues:
        #check for essential implicants
        essentials = []
        for item in trueValues:
            essentialImpl = False
            key = ''
            for k, lst in chart.items():
                if item in lst:
                    if not essentialImpl:
                        essentialImpl = True
                        key = k
                    else:
                        essentialImpl = False
                        break
            if essentialImpl:
                essentials.append(key)
        #remove implicants represented by essential terms from list
        if not essentials:
            break
        while essentials:
            key = essentials.pop()
            v = chart[key]
            result.append(key)
            for item in v:
                if item not in toDelete:
                    toDelete.append(item)
        while toDelete:
            trueValues.remove(toDelete.pop())
        #if some implicants are not represented by essential terms
        #leave in chart only implicants in which every item from
        #possible values list is still in trueValues
        if trueValues and firstLoop:
            firstLoop = False
            for k, lst in chart.items():
                delet = False
                for v in lst:
                    if v not in trueValues:
                        delet = True
                        break
                if delet:
                    toDelete.append(k)
        while toDelete:
            del chart[toDelete.pop()]
    #if there are still trueValues to be included in result
    #check possible sets of remaining implicants which cover trueValues
    remainingImpl = []
    for k, v in chart.items():
        remainingImpl.append(k)
    foundSet = False
    broke = False
    if trueValues:
        for i in range(1,len(remainingImpl)+1):
            if foundSet: break
            for possibleSet in itertools.combinations(remainingImpl,i):
                if foundSet: break
                broke = False
                for val in trueValues:
                    if not can_be_represented(val,possibleSet):
                        broke = True
                        break
                if not broke:
                    for item in possibleSet:
                        if item not in result:
                            result.append(item)
                    foundSet = True
    #change strings in list to minimal bool
    #result - list, variables - characters
    minimal = ''
    firstItem = True
    result = get_unique(result)
    for item in result:
        if not firstItem: minimal += ' + '
        else: firstItem = False
        minimal += turn_to_expr(item,variables)
    print("Minimal boolean expression:")
    print(minimal)
    

if __name__ == '__main__':
    main()
    
