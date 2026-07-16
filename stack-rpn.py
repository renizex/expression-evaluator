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

def plus(a: int | float, b: int | float) -> int | float:
    return a+b

def minus(a: int | float, b: int | float) -> int | float:
    return a-b

def multiply(a: int | float, b: int | float) -> int | float:
    return a*b

def divide(a: int | float, b: int | float) -> int | float:
    if b != 0:
        return a/b
    raise DivideByZeroError("ERROR: division by zero")

operations = {
    "+": plus,
    "-": minus,
    "*": multiply,
    "/": divide
}

def user_help() -> None:
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

def example() -> None:
    print("\nthis evaluator uses a notation called RPN - Reverse Polish Notation.")
    print("soon you will be able to change MODE to INFIX. what is 'INFIX'? it is a traditional '2 + 2' notation method.")
    print("so, how does RPN work? well, you can't just enter '2 + 2' here. you will get the 'this expression is logically incorrect' error.")
    print("instead, you need to enter an expression in this notation: '2 2 +' it equals 4.")
    print("more difficult expression: instead of '5 * 6 + 4', you need to enter '5 6 * 4 +'. both equals 34.")
    print("hope you got the idea. press enter to return at the 'help' menu.")
    input("> ")

def infix() -> None:
    print("\nWORK IN PROGRESS")
    print("(press enter to forget what you just saw)")
    input("> ")

def show_commands() -> None:
    print("\nmemory - see your memory.")
    print("clear - clear your memory.")
    print("what is memory? a variable store. you can see all your variables in memory.")

help_options = {
    "1": example,
    "2": infix,
    "3": show_commands
}

def main() -> None:
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
            result = evaluate(answer.split(), memory)
            if result["should_print"]:
                continue
            input_result = result["stack"].pop()
            print(f"your answer: {input_result}")
        except EvaluationError as msg:
            print(msg)

def show_memory(memory: dict[str, int | float]) -> None:
    if memory:
        for key, value in memory.items():
            print(f"{key} = {value}")
    else:
        print("memory is empty")

def clear_memory(memory: dict[str, int | float]) -> None:
    memory.clear()
    print("memory cleared")

main_options = {
    "memory": show_memory,
    "clear": clear_memory,
    "help": user_help
}

def evaluate(tokens: list[str], memory: dict[str, int | float]):
    stack = []
    should_print = True
    result = {
        "stack": stack,
        "should_print": should_print
    }
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
                        result["should_print"] = False
                        continue
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
                        result["should_print"] = True
                else:
                    raise OperatorError(f"ERROR: unknown operator '{token}'\nif stuck, learn RPN in help -> explanation\nstack: {stack}")
            else:
                raise EvaluationError(f"ERROR: operator '{token}' requires two operands.\nif stuck, learn RPN in help -> explanation\nstack: {stack}")
    if len(stack) != 1 and result["should_print"]:
        raise InvalidExpressionError(f"ERROR: expected one element in stack, got {len(stack)}\nif stuck, learn RPN in help -> explanation\nstack: {stack}")
    return result

def parse_number(token: str) -> tuple[int | float | str, str]:
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

def is_valid_variable(variable: str) -> bool:
    if variable:
        if not variable[0].isdigit():
            if all(char.isdigit() or char.isalpha() or char == "_" for char in variable):
                return True
    return False

main()
