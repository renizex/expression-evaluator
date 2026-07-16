class EvaluationError(Exception):
    pass

class InvalidExpressionError(EvaluationError):
    pass

class OperatorError(EvaluationError):
    pass

class DivideByZeroError(EvaluationError):
    pass

class InvalidVariableError(EvaluationError):
    pass

def plus(a, b):
    return a+b

def minus(a, b):
    return a-b

def multiply(a, b):
    return a*b

def divide(a, b):
    if b != 0:
        return a/b
    raise DivideByZeroError("ERROR: division by zero")

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
        print("3. commands")
        print("4. exit")
        answer = input("> ")
        if answer in help_options:
            help_options[answer]()
        elif answer == "4":
            return
        else:
            print("unknown command")

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

def show_commands():
    print("\nmemory - see your memory.")
    print("clear - clear your memory.")
    print("what is memory? a variable store. you can see all your variables in memory.")

help_options = {
    "1": example,
    "2": infix,
    "3": show_commands
}

def main():
    memory = {}
    print("RPN Calculator")
    print("enter 'help' for commands")
    while True:
        try:
            answer = input("> ")
            if answer in main_options:
                if answer in ["memory", "clear"]:
                    main_options[answer](memory)
                else:
                    main_options[answer]()
                continue
            if answer.strip() == '':
                print("ERROR: empty input")
                continue
            previous_memory = memory.copy()
            stack, memory = evaluate(answer.split(), memory)
            if previous_memory != memory:
                continue
            result = stack.pop()
            print(f"your answer: {result}")
        except EvaluationError as msg:
            print(msg)

def show_memory(memory):
    if memory:
        for key, value in memory.items():
            print(f"{key} = {value}")
    else:
        print("memory is empty")

def clear_memory(memory):
    memory.clear()
    print("memory cleared")

main_options = {
    "memory": show_memory,
    "clear": clear_memory,
    "help": user_help
}

def evaluate(tokens, memory):
    stack = []
    for token in tokens:
        number, symbol_type = parse_number(token)
        if symbol_type in ["integer", "float", "variable"]:
            stack.append(number)
        else:
            if len(stack) > 1:
                second_number = stack.pop()
                first_number = stack.pop()
                if token in ["+", "-", "*", "/", "="]:
                    if token == '=':
                        if not isinstance(first_number, str):
                            raise InvalidExpressionError("ERROR: left side of assignment is not a variable")
                        memory[first_number] = second_number
                        return stack, memory
                    else:
                        if isinstance(first_number, str):
                            if first_number in memory:
                                first_number = memory[first_number]
                            else:
                                raise InvalidExpressionError(f"ERROR: variable '{first_number}' does not exist.")
                        if isinstance(second_number, str):
                            if second_number in memory:
                                second_number = memory[second_number]
                            else:
                                raise InvalidExpressionError(f"ERROR: variable '{second_number}' does not exist.")
                        temporary_result = operations[token](first_number, second_number)
                        stack.append(temporary_result)
                else:
                    raise OperatorError(f"ERROR: unknown operator '{token}'\nif stuck, learn RPN in help -> explanation\nstack: {stack}")
            else:
                raise EvaluationError(f"ERROR: operator '{token}' requires two operands.\nif stuck, learn RPN in help -> explanation\nstack: {stack}")
    if not len(stack) == 1:
        raise InvalidExpressionError(f"ERROR: expected one element in stack, got {len(stack)}\nif stuck, learn RPN in help -> explanation\nstack: {stack}")
    return stack, memory

def parse_number(token):
    try:
        return int(token), "integer"
    except ValueError:
        try:
            return float(token), "float"
        except ValueError:
            if token in ["+", "-", "*", "/", "="]:
                return str(token), "operator"
            if is_valid_variable(str(token)):
                return token, "variable"
            else:
                raise InvalidVariableError(f"ERROR: invalid variable '{token}'")

def is_valid_variable(variable):
    if variable:
        if not variable[0].isdigit():
            if all(char.isdigit() or char.isalpha() or char == "_" for char in variable):
                return True
    return False

main()
