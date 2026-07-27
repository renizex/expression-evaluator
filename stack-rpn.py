from dataclasses import dataclass
from typing import TypeAlias, Literal, TypeGuard
import re

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
    if b == 0:
        raise DivideByZeroError("ERROR: division by zero")
    return a/b

def unary(a: Number) -> Number:
    return -a

operations = {
    "+": plus,
    "-": minus,
    "*": multiply,
    "/": divide,
}

OperatorStr = Literal["+", "-", "*", "/", "=", "u-"]
OPERATORS = {"+", "-", "*", "/", "=", "u-", "(", ")"}

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
    print("learn more about INFIX MODE in: 2. INFIX MODE.")
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
    is_infix = False
    print("RPN Calculator")
    if not is_infix:
        print("enter 'help' for commands or 'INFIX' to enter INFIX MODE.")
    else:
        print("enter 'help' for commands or 'RPN' to enter RPN MODE.")
    while True:
        try:
            answer = input("> ").strip()
            if answer in main_options:
                if answer in ["memory", "clear"]:
                    main_options[answer](memory)
                else:
                    main_options[answer]()
                continue
            elif answer.upper() == "INFIX":
                print("changed to INFIX MODE")
                is_infix = True
                continue
            elif answer.upper() == "RPN":
                print("changed to RPN MODE")
                is_infix = False
                continue
            if not pre_eval_main_input(answer):
                continue
            if is_infix:
                tokens = infix_to_rpn(tokenize_infix(answer.strip()))
            else:
                tokens = tokenize_rpn(answer.strip())
            input_result = evaluate(objectification(tokens), memory)
            if not input_result and input_result != 0:
                continue
            print(f"your answer: {input_result}")
        except EvaluationError as msg:
            print(msg)

VARIABLE_PATTERN = re.compile(r"-?[a-zA-Zа-яА-Я_]\w*")
NUMBER_PATTERN = re.compile(r"-?\d+\.?\d*")
OPERATOR_PATTERN = re.compile(r"[+\-*/=]")

def tokenize_rpn(answer: str) -> list[str]:
    raw_tokens = answer.split()
    tokens = []
    for token in raw_tokens:
        if NUMBER_PATTERN.fullmatch(token):
            tokens.append(token)
        elif VARIABLE_PATTERN.fullmatch(token):
            tokens.append(token)
        elif OPERATOR_PATTERN.fullmatch(token):
            tokens.append(token)
        else:
            raise InvalidExpressionError(f"ERROR: invalid RPN token - '{token}'")
    return tokens

def tokenize_infix(answer: str) -> list[str]:
    tokens = []
    raw_tokens = (re.split(r"([+\-*/=()\s])", answer))
    for token in raw_tokens:
        stripped_token = token.strip()
        if stripped_token:
            tokens.append(stripped_token)
    return tokens

OPERATOR_PRIORITY = {
    "=": 0,
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "u-": 3,
}

def infix_to_rpn(tokens: list[str]) -> list[str]:
    stack: list[str] = []
    output: list[str] = []
    prev_token: str | None = None
    for token in tokens:
        if token in OPERATORS:
            if token == "(":
                stack.append(token)
                continue
            elif token == ")":
                while stack:
                    if stack[-1] == "(":
                        break
                    output.append(stack.pop())
                if stack and stack[-1] == "(":
                    stack.pop()
                else:
                    raise InvalidExpressionError(f"ERROR: unmatched closing parenthesis\noutput: {output}")
                continue
            elif token == "-":
                if (
                        prev_token is None
                        or prev_token == "("
                        or prev_token in OPERATORS
                ):
                    stack.append("u-")
                    continue
            while (
                    stack
                    and stack[-1] != "("
                    and OPERATOR_PRIORITY[token] <= OPERATOR_PRIORITY[stack[-1]]
            ):
                output.append(stack.pop())
            stack.append(token)
        else:
            output.append(token)
        prev_token = token
    while stack:
        if stack[-1] == "(":
            raise InvalidExpressionError(f"ERROR: unmatched opening parenthesis\noutput: {output}")
        output.append(stack.pop())
    return output

def pre_eval_main_input(answer: str) -> bool:
    if answer.strip() == '':
        print("ERROR: empty input")
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
            if token.value == "u-":
                number = resolve_operand(stack.pop(), memory)
                temporary_result = create_number_token(unary(number))
                stack.append(temporary_result)
                continue
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
    raise InvalidExpressionError(f"ERROR: variable '{token.value}' does not exist.")

def objectification(raw_tokens: list[str]) -> list[Token]:
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
