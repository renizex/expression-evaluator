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

operators = ["+", "-", "*", "/", "="]

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
    print("hope you got the idea. press enter to return at the 'help' menu.\n")
    print("also, you can initialize a variable. example: 'x 5 ='. gives 'x = 5' in memory.")
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
            if not pre_eval_main_input(answer):
                continue
            input_result = evaluate(answer.split(), memory)
            if not input_result and input_result != 0:
                continue
            print(f"your answer: {input_result}")
        except EvaluationError as msg:
            print(msg)

def pre_eval_main_input(answer: str) -> bool:
    if answer.strip() == '':
        print("ERROR: empty input")
        return False
    separated = answer.split()
    if len(separated) == 1:
        print("ERROR: expression cannot be evaluated.")
        return False
    return True

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

def evaluate(tokens: list[str], memory: dict[str, int | float]) -> int | None:
    stack = []
    for token in tokens:
        number, symbol_type = parse_number(token)
        if symbol_type in ["integer", "float", "variable"]:
            stack.append(number)
        else:
            if len(stack) > 1:
                second_number = stack.pop()
                first_number = stack.pop()
                if token in operators:
                    if token == '=':
                        assign_value(first_number, second_number, memory)
                        continue
                    else:
                        first_number = resolve_operand(first_number, memory)
                        second_number = resolve_operand(second_number, memory)
                        temporary_result = operations[token](first_number, second_number)
                        stack.append(temporary_result)
                else:
                    raise OperatorError(f"ERROR: unknown operator '{token}'\nif stuck, learn RPN in help -> explanation\nstack: {stack}")
            else:
                raise EvaluationError(f"ERROR: operator '{token}' requires two operands.\nif stuck, learn RPN in help -> explanation\nstack: {stack}")
    if len(stack) > 1:
        raise InvalidExpressionError(f"ERROR: expected one element in stack, got {len(stack)}\nif stuck, learn RPN in help -> explanation\nstack: {stack}")
    elif len(stack) == 1:
        return stack[0]
    return None

def assign_value(first_value: str, second_value: int | float, memory: dict[str, int | float]):
    if not isinstance(first_value, str):
        raise InvalidExpressionError("ERROR: left side of assignment is not a variable")
    if isinstance(second_value, str):
        if second_value not in memory:
            raise InvalidExpressionError("ERROR: right side of assignment is not a number")
        else:
            second_value = memory[second_value]
    memory[first_value] = second_value

def resolve_operand(value: str | int | float, memory: dict[str, int | float]) -> int | float:
    if isinstance(value, str):
        if value in memory:
            return memory[value]
    else:
        return value
    raise InvalidExpressionError(f"ERROR: variable '{value}' does not exist.")

def parse_number(token: str) -> tuple[int | float | str, str]:
    try:
        return int(token), "integer"
    except ValueError:
        try:
            return float(token), "float"
        except ValueError:
            if token in operators:
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
