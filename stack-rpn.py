import re
from abc import ABC
from dataclasses import dataclass
from typing import TypeAlias, Literal, TypeGuard, Callable
import math

VARIABLE_PATTERN = re.compile(r"[a-zA-Zа-яА-Я_]\w*")
NUMBER_PATTERN = re.compile(r"-?\d+\.?\d*")
OPERATOR_PATTERN = re.compile(r"sqrt|u\^|[+\-*/=^]")

class EvaluationError(Exception):
    pass

class InvalidExpressionError(EvaluationError):
    pass

class DivideByZeroError(EvaluationError):
    pass

class InvalidVariableError(EvaluationError):
    pass

class SquareRootOfNegativeError(EvaluationError):
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

def unary_minus(a: Number) -> Number:
    return -a

def degree(a: Number, b: Number) -> Number:
    if a == 0 and b < 0:
        raise DivideByZeroError("ERROR: division by zero")
    return a**b

def square(a: Number) -> Number:
    return a*a

def sqrt(a: Number) -> Number:
    if a < 0:
        raise SquareRootOfNegativeError(f"ERROR: number '{a}' is negative")
    return math.sqrt(a)

OperatorStr: TypeAlias = Literal["+", "-", "*", "/", "=", "u-", "(", ")", "^", "u^", "sqrt"]

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

def assign_value(variable: VariableToken, number: Number, memory: Memory) -> None:
    memory[variable.value] = number

@dataclass(kw_only=True)
class OperatorInfo(ABC):
    priority: int

@dataclass(kw_only=True)
class ParenthesisOperatorInfo(OperatorInfo):
    function: None = None

@dataclass(kw_only=True)
class UnaryOperatorInfo(OperatorInfo):
    function: Callable[[Number], Number]

@dataclass(kw_only=True)
class BinaryOperatorInfo(OperatorInfo):
    function: Callable[[Number, Number], Number]

@dataclass(kw_only=True)
class AssignmentOperatorInfo(OperatorInfo):
    function: Callable [[VariableToken, Number, Memory], None]

OPERATORS = {
    "(": ParenthesisOperatorInfo(priority=-1),
    ")": ParenthesisOperatorInfo(priority=-1),
    "=": AssignmentOperatorInfo(priority=0, function=assign_value),
    "+": BinaryOperatorInfo(priority=1, function=plus),
    "-": BinaryOperatorInfo(priority=1, function=minus),
    "*": BinaryOperatorInfo(priority=2, function=multiply),
    "/": BinaryOperatorInfo(priority=2, function=divide),
    "u-": UnaryOperatorInfo(priority=3, function=unary_minus),
    "^": BinaryOperatorInfo(priority=4, function=degree),
    "u^": UnaryOperatorInfo(priority=5, function=square),
    "sqrt": UnaryOperatorInfo(priority=6, function=sqrt),
}

def help_main() -> None:
    while True:
        print("\nthis is a help page.")
        print("what do you seek?")
        print("1. an example and an explanation if i'm stuck.")
        print("2. INFIX MODE")
        print("3. commands")
        print("4. operators")
        print("5. exit")
        answer = input("> ")
        if answer in help_menu:
            help_menu[answer]()
        elif answer == "5":
            return
        else:
            print("\nunknown command.")

def help_explanation() -> None:
    print("\nthis evaluator uses a notation called RPN - Reverse Polish Notation.")
    print("now you can change MODE to INFIX. what is 'INFIX'? it is a traditional '2 + 2' notation method.")
    print("so, how does RPN work? well, you can't just enter '2 + 2' here. you will get the 'this expression is logically incorrect' error.")
    print("instead, you need to enter an expression in this notation: '2 2 +' it equals 4.")
    print("more difficult expression: instead of '5 * 6 + 4', you need to enter '5 6 * 4 +'. both equals 34.")
    print("hope you got the idea. press enter to return at the 'help' menu.\n")
    print("learn more about INFIX MODE in: 2. INFIX MODE.")
    print("also, you can initialize a variable. example: 'x 5 ='. gives 'x = 5' in memory.")
    input("> ")

def help_infix() -> None:
    print("\nINFIX MODE is a notation that acts just like regular calculators.")
    print("instead of typing '2 2 +', you can just type '2 + 2' like you traditionally do.")
    print("parentheses () and unary minus are now supported.")
    print("examples:")
    print("2 + 2")
    print("2 + 3 * 4")
    print("5 * 6 / 7")
    print("5 + (10 * 5)")
    print("-5 - (200 + 400)")
    print("5 ^ 4")
    print("sqrt(sqrt(256)) + 5^ ('5^' automatically squares the number 5)")
    print("enable this mode by typing 'INFIX' in the main menu.")
    input("> ")

def help_operators() -> None:
    print("\nall of operators are similar to RPN and INFIX MODES.")
    print("'+' - plus")
    print("'-' - minus")
    print("'*' - multiply")
    print("'/' - divide")
    print("'^' - exponentiation")
    print("'u^' - square (RPN only)")
    print("'=' - assign")
    print("'sqrt' - square root of the expression")
    input("> ")

def help_commands() -> None:
    print("\nINFIX - switch to INFIX MODE.")
    print("RPN - switch to RPN MODE")
    print("\nmemory - see your memory.")
    print("clear - clear your memory.")
    print("what is memory? a variable store. you can see all your variables in memory.")

help_menu = {
    "1": help_explanation,
    "2": help_infix,
    "3": help_commands,
    "4": help_operators
}

def main() -> None:
    memory: Memory = {}
    is_infix = True
    print("RPN Calculator")
    print(f"you are in {mode_output(is_infix)}")
    print("enter 'help' for commands")
    print("enter 'INFIX' to enter INFIX MODE")
    print("enter 'RPN' to enter RPN MODE")
    while True:
        try:
            answer = input("> ").strip()
            is_continue, is_infix = main_processing(answer, memory, is_infix)
            if is_continue:
                continue
            tokens = lex_expression(answer, is_infix)
            output_result = evaluate(parse_tokens(tokens), memory)
            if output_result is None:
                continue
            print(f"your answer: {normalize_number(output_result)}")
        except EvaluationError as msg:
            print(msg)
        except OverflowError:
            print("ERROR: number is too large to calculate.")

def mode_output(is_infix: bool) -> str:
    if is_infix:
        return "INFIX MODE"
    return "RPN MODE"

def main_processing(answer: str, memory: Memory, is_infix: bool) -> tuple[bool, bool]:
    if answer.strip() == '':
        print("ERROR: empty input")
        return True, is_infix
    if answer in main_options:
        if answer in ["memory", "clear"]:
            main_options[answer](memory)
        else:
            main_options[answer]()
        return True, is_infix
    elif answer.upper() == "INFIX":
        print("changed to INFIX MODE")
        return True, True
    elif answer.upper() == "RPN":
        print("changed to RPN MODE")
        return True, False
    return False, is_infix

def normalize_number(value: Number | None) -> Number | None:
    if value is None:
        return None
    match value:
        case int():
            return value
        case float():
            clean_value = round(value, 12)
            if clean_value % 1 == 0:
                return int(clean_value)
            return clean_value

def lex_expression(expression: str, is_infix: bool) -> list[str]:
    if is_infix:
        return infix_to_rpn(lex_infix(expression))
    return lex_rpn(expression)

def lex_rpn(expression: str) -> list[str]:
    raw_lexemes = expression.split()
    lexemes = []
    for lexeme in raw_lexemes:
        if NUMBER_PATTERN.fullmatch(lexeme):
            lexemes.append(lexeme)
        elif VARIABLE_PATTERN.fullmatch(lexeme):
            lexemes.append(lexeme)
        elif OPERATOR_PATTERN.fullmatch(lexeme):
            lexemes.append(lexeme)
        else:
            raise InvalidExpressionError(f"ERROR: invalid RPN symbol - '{lexeme}'")
    return lexemes

def lex_infix(expression: str) -> list[str]:
    lexemes = []
    raw_tokens = (re.split(r"([+\-*/=()^\s])", expression))

    for symbol in raw_tokens:
        stripped_symbol = symbol.strip()
        if stripped_symbol:
            lexemes.append(stripped_symbol)
    return lexemes

def infix_to_rpn(lexemes: list[str]) -> list[str]:
    stack: list[str] = []
    output: list[str] = []
    prev_lexeme: str | None = None
    for index, lexeme in enumerate(lexemes):
        if lexeme in OPERATORS:
            if lexeme == "(":
                stack.append(lexeme)
                continue
            elif lexeme == ")":
                while stack:
                    if stack[-1] == "(":
                        break
                    output.append(stack.pop())
                if stack and stack[-1] == "(":
                    stack.pop()
                else:
                    raise InvalidExpressionError(f"ERROR: unmatched closing parenthesis.")
                continue
            elif lexeme == "-":
                if (
                        prev_lexeme is None
                        or prev_lexeme == "("
                        or prev_lexeme in OPERATORS
                ):
                    stack.append("u-")
                    continue
            elif lexeme == "^":
                next_lexeme = None if index == len(lexemes) - 1 else lexemes[index + 1]
                after_next = None if index >= len(lexemes) - 2 else lexemes[index + 2]
                is_next_unary_minus = (
                    next_lexeme == "-"
                    and after_next is not None
                    and (after_next not in OPERATORS or after_next == "(")
                )
                if (
                        prev_lexeme
                        and prev_lexeme not in OPERATORS
                        and (next_lexeme is None or next_lexeme in OPERATORS and next_lexeme != "(" and not is_next_unary_minus)
                ):
                    stack.append("u^")
                    continue
            while stack and stack[-1] != "(":
                current = OPERATORS[lexeme]
                top = OPERATORS[stack[-1]]
                if current.priority < top.priority or (current.priority == top.priority and not is_right_associativity(lexeme)):
                    output.append(stack.pop())
                else:
                    break
            stack.append(lexeme)
        else:
            output.append(lexeme)
        prev_lexeme = lexeme
    while stack:
        if stack[-1] == "(":
            raise InvalidExpressionError(f"ERROR: unmatched opening parenthesis.")
        output.append(stack.pop())
    return output

def is_right_associativity(lexeme: str) -> bool:
    return lexeme in ['^', 'u^']

def show_memory(memory: Memory) -> None:
    if memory:
        for key, value in memory.items():
            print(f"{key} = {normalize_number(value)}")
    else:
        print("memory is empty")

def clear_memory(memory: Memory) -> None:
    memory.clear()
    print("memory cleared")

main_options = {
    "memory": show_memory,
    "clear": clear_memory,
    "help": help_main
}

def evaluate(tokens: list[Token], memory: Memory) -> Number | None:
    stack: list[Operand] = []
    for token in tokens:
        if isinstance(token, (IntegerToken, FloatToken, VariableToken)):
            stack.append(token)
        else:
            operator = OPERATORS[token.value]
            match operator:
                case UnaryOperatorInfo():
                    a = pop_operand(stack, memory, token)
                    temporary_result = create_number_token(operator.function(a))
                    stack.append(temporary_result)
                    continue
                case BinaryOperatorInfo():
                    a, b = pop_two_operands(stack, memory, token)
                    calculated_result = operator.function(a, b)
                    temporary_result = create_number_token(calculated_result)
                    stack.append(temporary_result)
                case AssignmentOperatorInfo():
                    b = pop_operand(stack, memory, token)
                    a = pop_assignable(stack, token)
                    operator.function(a, b, memory)
                    continue
    if len(stack) > 1:
        raise InvalidExpressionError(f"ERROR: expected one element in stack, got {len(stack)}\nif stuck, learn RPN in help -> explanation.")
    elif len(stack) == 1:
        return resolve_operand(stack[0], memory)
    return None

def pop_operand(stack: list[Operand], memory: Memory, token: Token) -> Number:
    if not stack:
        raise EvaluationError(f"ERROR: operator '{token.value}' requires one operand.\nif stuck, learn RPN in help -> explanation.")
    operand = stack.pop()
    return resolve_operand(operand, memory)

def pop_two_operands(stack: list[Operand], memory: Memory, token: Token) -> tuple[Number, Number]:
    if not len(stack) > 1:
        raise EvaluationError(f"ERROR: operator '{token.value}' requires two operands.\nif stuck, learn RPN in help -> explanation.")
    second_operand = stack.pop()
    first_operand = stack.pop()
    return resolve_operand(first_operand, memory), resolve_operand(second_operand, memory)

def pop_assignable(stack: list[Operand], token: Token) -> VariableToken:
    if not stack:
        raise EvaluationError(f"ERROR: operator '{token.value}' requires two operands.\nif stuck, learn RPN in help -> explanation.")
    variable = stack.pop()
    if not isinstance(variable, VariableToken):
        raise InvalidVariableError(f"ERROR: expected variable got '{variable.value}'")
    return variable

def create_number_token(number: int | float) -> IntegerToken | FloatToken:
    match number:
        case int():
            return IntegerToken(number)
        case float():
            return FloatToken(number)
        case complex():
            raise InvalidExpressionError(f"ERROR: unexpected complex number '{number}'")
        case _:
            raise InvalidExpressionError(f"ERROR: expected integer or float, got {type(number)}")

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

def parse_tokens(lexemes: list[str]) -> list[Token]:
    tokens: list[Token] = []
    for lexeme in lexemes:
        tokens.append(parse_lexeme(lexeme))
    return tokens

def parse_lexeme(lexeme: str) -> Token:
    try:
        return IntegerToken(value=int(lexeme))
    except ValueError:
        try:
            return FloatToken(value=float(lexeme))
        except ValueError:
            if is_operator(lexeme):
                return OperatorToken(value=lexeme)
            elif is_valid_variable(str(lexeme)):
                return VariableToken(value=lexeme)
            else:
                raise InvalidVariableError(f"ERROR: invalid variable '{lexeme}'")

def is_operator(lexeme: str) -> TypeGuard[OperatorStr]:
    return lexeme in OPERATORS

def is_valid_variable(variable: str) -> bool:
    if variable:
        if not variable[0].isdigit():
            if all(char.isdigit() or char.isalpha() or char == "_" for char in variable):
                return True
    return False

if __name__ == '__main__':
    main()
