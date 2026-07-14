def plus(a, b):
    return a+b

def minus(a, b):
    return a-b

def multiply(a, b):
    return a*b

def divide(a, b):
    if b != 0:
        return a/b
    raise ValueError("ERROR: division by zero")

operations = {
    "+": plus,
    "-": minus,
    "*": multiply,
    "/": divide
}

def user_help():
    while True:
        print("\nthis is a help page.")
        print("what do you seek?")
        print("1. an example and an explanation if i'm stuck.")
        print("2. INFIX MODE")
        print("3. exit")
        answer = input("> ")
        if answer in options:
            options[answer]()
        elif answer == "3":
            return

def example():
    print("\nthis evaluator uses a notation called RPN - Reverse Polish Notation.")
    print("soon you will be able to change MODE to INFIX. what is 'INFIX'? it is a traditional '2 + 2' notation method.")
    print("so, how does RPN work? well, you can't just enter '2 + 2' here. you will get the 'this expression is logically incorrect' error.")
    print("instead, you need to enter an expression in this notation: '2 2 +' it equals 4.")
    print("more difficult expression: instead of '5 * 6 + 4', you need to enter '5 6 * 4 +'. both equals 34.")
    print("hope you got the idea. press enter to return at the 'help' menu.")
    input("> ")

def infix():
    print("\nWORK IN PROGRESS")
    print("(press enter to forget what you just saw)")
    input("> ")

options = {
    "1": example,
    "2": infix,
}

def main():
    print("enter 'help' to see available options")
    while True:
        try:
            error_flag = False
            stack = []
            answer = input("> ")
            if answer == "help":
                user_help()
                continue
            if not answer or answer.strip() == "":
                print("ERROR: empty input")
                continue
            separation = answer.split()
            for token in separation:
                if token.isdigit():
                    stack.append(int(token))
                else:
                    if len(stack) > 1:
                        second_number = stack.pop()
                        first_number = stack.pop()
                        if token in operations:
                            temporary_result = operations[token](first_number, second_number)
                            stack.append(temporary_result)
                        else:
                            print(f"ERROR: unknown operator '{token}'")
                            print(stack)
                            error_flag = True
                            break
                    else:
                        print(f"ERROR: not enough operands for operand {token} (at least 2)")
                        print(stack)
                        error_flag = True
                        break
            if error_flag:
                continue
            elif not len(stack) == 1:
                print(f"ERROR: expected one element in stack, got {len(stack)}")
                print(stack)
                continue
            final_result = stack.pop()
            print(f"your answer: {final_result}")
        except ValueError as msg:
            print(msg)
            continue

main()
