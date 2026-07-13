def plus(a, b):
    return a+b

def minus(a, b):
    return a-b

def multiply(a, b):
    return a*b

def divide(a, b):
    if b != 0:
        return a/b
    raise ValueError("division by zero")

operations = {
    "+": plus,
    "-": minus,
    "*": multiply,
    "/": divide
}

def main():
    while True:
        try:
            digits_count = 0
            operators_count = 0
            error_flag = False
            stack = []
            answer = input("> ")
            if not answer or answer.strip() == "":
                print("you didn't write anything")
                continue
            separation = answer.split()
            for token in separation:
                if token.isdigit():
                    digits_count += 1
                    stack.append(int(token))
                else:
                    operators_count += 1
                    if len(stack) > 1:
                        second_number = stack.pop()
                        first_number = stack.pop()
                        if token in operations:
                            temporary_result = operations[token](first_number, second_number)
                            stack.append(temporary_result)
                        else:
                            print("unknown operator")
                            error_flag = True
                            break
                    else:
                        print("not enough numbers in stack")
                        error_flag = True
                        break
            if digits_count != operators_count + 1 and not error_flag:
                print("this expression is logically incorrect")
                error_flag = True
            if error_flag:
                continue
            else:
                final_result = stack.pop()
                print(f"your answer: {final_result}")
        except ValueError as msg:
            print(msg)
            continue

main()
