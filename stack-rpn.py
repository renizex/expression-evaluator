from dataclasses import dataclass
from typing import TypeAlias, Literal, TypeGuard


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

Number: TypeAlias = int | float
Memory: TypeAlias = dict[str, Number]

def plus(a: Number, b: Number) -> Number:
    return a+b

def minus(a: Number, b: Number) -> Number:
    return a-b

def multiply(a: Number, b: Number) -> Number:
    return a*b

def divide(a: Number, b: Number) -> Number:
    if b != 0:
        return a/b
    raise DivideByZeroError("ERROR: division by zero")

operations = {
    "+": plus,
    "-": minus,
    "*": multiply,
    "/": divide
}

OperatorStr = Literal["+", "-", "*", "/", "="]
OPERATORS: set[OperatorStr] = {"+", "-", "*", "/", "="}

@dataclass
class IntegerToken:
    value: int

@dataclass
class FloatToken:
    value: float

@dataclass
class OperatorToken:
    value: OperatorStr

@dataclass
class VariableToken:
    value: str

Token: TypeAlias = IntegerToken | FloatToken | OperatorToken | VariableToken
Operand: TypeAlias = IntegerToken | FloatToken | VariableToken

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
    memory: Memory = {}
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
            input_result = evaluate(tokenize(answer.split()), memory)
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

def show_memory(memory: Memory) -> None:
    if memory:
        for key, value in memory.items():
            print(f"{key} = {value}")
    else:
        print("memory is empty")

def clear_memory(memory: Memory) -> None:
    memory.clear()
    print("memory cleared")

main_options = {
    "memory": show_memory,
    "clear": clear_memory,
    "help": user_help
}

def evaluate(tokens: list[Token], memory: Memory) -> Number | None:
    stack: list[Operand] = []
    for token in tokens:
        if isinstance(token, (IntegerToken, FloatToken, VariableToken)):
            stack.append(token)
        else:
            if len(stack) > 1:
                second_number = stack.pop()
                first_number = stack.pop()
                if token.value == '=':
                    assign_value(first_number, second_number, memory)
                    continue
                else:
                    first_number = resolve_operand(first_number, memory)
                    second_number = resolve_operand(second_number, memory)
                    temporary_result = create_number_token(operations[token.value](first_number, second_number))
                    stack.append(temporary_result)
            else:
                raise EvaluationError(f"ERROR: operator '{token.value}' requires two operands.\nif stuck, learn RPN in help -> explanation\nstack: {stack}")
    if len(stack) > 1:
        raise InvalidExpressionError(f"ERROR: expected one element in stack, got {len(stack)}\nif stuck, learn RPN in help -> explanation\nstack: {stack}")
    elif len(stack) == 1:
        return resolve_operand(stack[0], memory)
    return None

def create_number_token(number: int | float) -> IntegerToken | FloatToken:
    match number:
        case int():
            return IntegerToken(number)
        case float():
            return FloatToken(number)
        case _:
            raise InvalidExpressionError(f"ERROR: expected integer or float, got {type(number)}")

def assign_value(first_token: Token, second_token: Operand, memory: Memory):
    match first_token:
        case VariableToken(name):
            number = resolve_operand(second_token, memory)
            memory[name] = number
            return
    raise InvalidExpressionError("ERROR: left side of assignment is not a variable.")

def resolve_operand(token: Operand, memory: Memory) -> Number:
    match token:
        case IntegerToken(number):
            return number
        case FloatToken(number):
            return number
        case VariableToken(name):
            if name in memory:
                return memory[name]
    raise InvalidExpressionError(f"ERROR: variable '{token}' does not exist.")

def tokenize(raw_tokens: list[str]) -> list[Token]:
    tokens: list[Token] = []
    for raw in raw_tokens:
        tokens.append(parse_token(raw))
    return tokens

def parse_token(raw: str) -> Token:
    try:
        return IntegerToken(value=int(raw))
    except ValueError:
        try:
            return FloatToken(value=float(raw))
        except ValueError:
            if is_operator(raw):
                return OperatorToken(value=raw)
            elif is_valid_variable(str(raw)):
                return VariableToken(value=raw)
            else:
                raise InvalidVariableError(f"ERROR: invalid variable '{raw}'")

def is_operator(token: str) -> TypeGuard[OperatorStr]:
    return token in OPERATORS

def is_valid_variable(variable: str) -> bool:
    if variable:
        if not variable[0].isdigit():
            if all(char.isdigit() or char.isalpha() or char == "_" for char in variable):
                return True
    return False

main()
