def plus(a, b):
    return a+b

def minus(a, b):
    return a-b

def multiply(a, b):
    return a*b

def divide(a, b):
    return a/b

operations = {
    "+": plus,
    "-": minus,
    "*": multiply,
    "/": divide
}

def main():
    while True:
        answer = ""
        digits = []
        operators = []
        print("enter the expression")
        result = input("> ").strip()
        if result == "":
            print("error")
            continue
        separation = result.split()
        for expression in separation:
            if expression.isdigit():
                digits.append(int(expression))
            elif expression in ["+", "-", "*", "/"]:
                operators.append(expression)
            else:
                print("you entered an invalid expression")
                continue

        while operators:
            op1 = len(operators) + 1
            op2 = len(operators) + 1
            op3 = len(operators) + 1
            op4 = len(operators) + 1
            if "*" in operators:
                op2 = operators.index("*")
            if "/" in operators:
                op1 = operators.index("/")
            if "-" in operators:
                op4 = operators.index("-")
            if "+" in operators:
                op3 = operators.index("+")
            op = min(op1, op2)
            if op ==  len(operators) + 1:
                op = min(op3, op4)
            n1 = digits[op]
            n2 = digits[op + 1]
            if operators[op] == "/" and n2 == 0:
                print("you cannot divide by zero")
                break
            answer = operations[operators[op]](n1, n2)
            digits[op:op + 2] = [answer]
            operators.pop(op)
        print(answer)

main()
