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
        digits_count = 0
        operators_count = 0
        error_flag = False
        stack = []
        answer = input("> ")
        if not answer or answer.strip() == "":
            print("you didn't write anything")
            continue
        separation = answer.split()
        if len(separation) < 3:
            print("expression is too short")
            continue
        for token in separation:
            if token.isdigit():
                digits_count += 1
            else:
                operators_count += 1
        if digits_count != operators_count + 1:
            print("this expression logically incorrect")
            continue
        for token in separation:
            if token.isdigit():
                stack.append(int(token))
            else:
                if len(stack) > 1:
                    second_number = stack.pop()
                    first_number = stack.pop()
                    temporary_result = operations[token](first_number, second_number)
                    stack.append(temporary_result)
                else:
                    print("not enough numbers in stack")
                    error_flag = True
                    break
        if error_flag:
            continue
        elif len(stack) > 1:
            print("invalid expression")
            continue
        else:
            final_result = stack.pop()
            print(f"your answer: {final_result}")


main()