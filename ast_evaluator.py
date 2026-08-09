import re
from dataclasses import dataclass
from typing import TypeAlias, NoReturn

class InvalidExpressionError(Exception):
    pass

class InvalidLexemeError(InvalidExpressionError):
    pass

class DivisionByZeroError(InvalidExpressionError):
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
        raise DivisionByZeroError("ERROR: division by zero")
    return a/b

def power(a: Number, b: Number) -> Number:
    if a == 0 and b < 0:
        raise DivisionByZeroError("ERROR: division by zero")
    return a**b

def equal(a: Number, b: Number) -> bool:
    return a == b

def greater(a: Number, b: Number) -> bool:
    return a > b

def less(a: Number, b: Number) -> bool:
    return a < b

operations = {
    '+': plus,
    '-': minus,
    '*': multiply,
    '/': divide,
    '^': power
}

comparison = {
    '==': equal,
    '>': greater,
    '<': less
}

def unary_minus(a: Number) -> Number:
    return -a

@dataclass
class Token:
    value: str
    position: int

@dataclass
class BinaryOperatorToken(Token):
    pass

@dataclass
class AssignToken(Token):
    pass

@dataclass
class OpeningParenthesisToken(Token):
    pass

@dataclass
class ClosingParenthesisToken(Token):
    pass

@dataclass
class NumberToken(Token):
    value: Number

@dataclass
class VariableToken(Token):
    pass

@dataclass
class EqualToken(Token):
    pass

@dataclass
class IfToken(Token):
    pass

@dataclass
class ElseToken(Token):
    pass

@dataclass
class WhileToken(Token):
    pass

@dataclass
class OpeningBraceToken(Token):
    pass

@dataclass
class ClosingBraceToken(Token):
    pass

@dataclass
class Node:
    pass

@dataclass
class BinaryOperatorNode(Node):
    left: Node
    operator: str
    right: Node

@dataclass
class NumberNode(Node):
    value: Number

@dataclass
class VariableNode(Node):
    value: str

@dataclass
class UnaryMinusNode(Node):
    operand: Node

@dataclass
class AssignNode(Node):
    variable: VariableNode
    operator: str
    right: Node

@dataclass
class BlockNode(Node):
    block: list[Node]

@dataclass
class IfNode(Node):
    condition: Node
    body: BlockNode
    else_body: BlockNode | None

@dataclass
class WhileNode(Node):
    condition: Node
    body: BlockNode
    else_body: BlockNode | None

def memory_show(memory: dict[str, Number]) -> str:
    if not memory:
        return "memory is empty"
    return '\n'.join(f"{variable} = {number}" for variable, number in memory.items())

def memory_clear(memory: dict[str, Number]) -> str:
    memory.clear()
    return "memory cleared"

def help_show() -> str:
    return """
commands:
    memory: show memory
    clear: clear memory
    help: show this
        
operators:
    basic:
        '+', '-', '*', '/' including unary minus
    '^': power
    '=': assign
    '(', ')': parentheses
    'if', 'else', '<', '>', '=='
    example:
        > x = 5
        > y = 6
        > if x > y {x+y} else {x-y}
        output: 
            -1
    
planned:
    functions.
    """.strip()

memory_commands = {
    "memory": memory_show,
    "clear": memory_clear
}

help_commands = {
    "help": help_show
}

def main() -> None:
    memory: dict[str, Number] = {}
    print("AST evaluator")
    print("enter 'help' for commands and operators")
    while True:
        try:
            expression = input("> ")
            if check_expression(expression, memory):
                continue
            tokens = lex(expression)
            node = parse(tokens, expression)
            output = evaluate(node, memory)
            if output is None:
                continue
            print(output)
        except InvalidExpressionError as msg:
            print(msg)

def check_expression(expression: str, memory: Memory) -> bool:
    if is_command(expression, memory):
        return True
    if expression.strip() == '':
        raise InvalidExpressionError(f"ERROR: empty input.")
    return False

def is_command(expression: str, memory: Memory) -> bool:
    if expression in memory_commands:
        print(memory_commands[expression](memory))
        return True
    elif expression in help_commands:
        print(help_commands[expression]())
        return True
    return False

def lex(expression: str) -> list[Token]:
    tokens: list[Token] = []
    matches = re.finditer(r"(\d+\.\d+|\d+)|([A-Za-z_]\w*)|(==|[+\-*/=()^><{}])|(\s+)|(.)", expression)
    for match in matches:
        if match.group(1):
            raw_number = match.group(1)
            number = float(raw_number) if '.' in raw_number else int(raw_number)
            tokens.append(NumberToken(number, match.start()))
        elif match.group(2):
            variable = match.group(2)
            if variable in keywords:
                tokens.append(keywords[variable](variable, match.start()))
            else:
                tokens.append(VariableToken(variable, match.start()))
        elif match.group(3):
            operator = match.group(3)
            if operator in special_operators:
                tokens.append(special_operators[operator](operator, match.start()))
            else:
                tokens.append(BinaryOperatorToken(operator, match.start()))
        elif match.group(4):
            pass
        elif match.group(5):
            raise InvalidLexemeError(f"ERROR: unknown lexeme '{match.group(5)}' at position {match.start()}.")
    return tokens

keywords = {
    'if': IfToken,
    'else': ElseToken,
    'while': WhileToken
}

special_operators = {
    '==': EqualToken,
    '=': AssignToken,
    '(': OpeningParenthesisToken,
    ')': ClosingParenthesisToken,
    '{': OpeningBraceToken,
    '}': ClosingBraceToken
}

def parse(tokens: list[Token], expression: str) -> Node:
    parser = Parser(tokens, expression)
    node = parser.parse_statement()
    return node

class Parser:
    def __init__(self, tokens: list[Token], expression: str) -> None:
        self.tokens = tokens
        self.expression = expression
        self.current_index = 0

    def current(self) -> Token | None:
        #print(self.current_index, len(self.tokens))
        if self.current_index >= len(self.tokens):
            return None
        return self.tokens[self.current_index]

    def previous(self) -> Token | None:
        if self.current_index > 0:
            return self.tokens[self.current_index - 1]
        return None

    def advance(self) -> None:
        self.current_index += 1

    def error(self, message: str) -> NoReturn:
        current = self.current()
        previous = self.previous()
        if current is not None:
            pointer = ' ' * current.position + '^' if self.current_index else '^'
        elif previous is not None:
            pointer = ' ' * previous.position + '^' if self.current_index else '^'
        else:
            pointer = '^'
        raise InvalidExpressionError(
            f"      {message}\n"
            f"      {self.expression}\n"
            f"      {pointer}"
        )

    def match(self, *values: str) -> bool:
        current = self.current()
        return current is not None and current.value in values

    def consume(self, *values: str) -> str | None:
        current = self.current()
        if current is None:
            return None
        if current.value not in values:
            return None
        self.advance()
        return current.value

    def expect(self, *args) -> bool:
        current = self.current()
        if current is not None:
            if current.value in args:
                return True
            self.error(f"ERROR: expected {args}, got {current.value}.")
        return False

    def parse_statement(self) -> Node:
        current = self.current()
        match current:
            case IfToken():
                self.advance()
                return self.parse_if_statement()
            case WhileToken():
                self.advance()
                return self.parse_while_statement()
            case _:
                return self.parse_assignment()

    def parse_if_statement(self) -> Node:
        condition = self.parse_expression()
        body = self.parse_block()
        if self.consume('else') is None:
            return IfNode(condition, body, None)
        else_body = self.parse_block()
        return IfNode(condition, body, else_body)

    def parse_while_statement(self) -> Node:
        condition = self.parse_expression()
        body = self.parse_block()
        if self.consume('else') is None:
            return WhileNode(condition, body, None)
        else_body = self.parse_block()
        return WhileNode(condition, body, else_body)

    def parse_block(self) -> BlockNode:
        block: list[Node] = []
        if self.consume('{') is None:
            self.error(f"ERROR: expected '{'{'}', got 'None'.")
        while True:
            current = self.current()
            if current is None:
                self.error(f"ERROR: expected {'}'}, got 'None'")
            if current.value == '}':
                break
            block.append(self.parse_statement())
        self.consume('}')
        return BlockNode(block)

    def parse_assignment(self) -> Node:
        variable = self.parse_expression()
        while True:
            operator = self.consume('=')
            if operator is None:
                break
            if not isinstance(variable, VariableNode):
                self.error(f"ERROR: expected a variable, got '{variable}'.")
            right = self.parse_expression()
            variable = AssignNode(variable, operator, right)
        return variable

    def parse_expression(self) -> Node:
        left = self.parse_comparison()
        while True:
            operator = self.consume('+', '-')
            if operator is None:
                break
            right = self.parse_comparison()
            left = BinaryOperatorNode(left, operator, right)
        return left

    def parse_comparison(self) -> Node:
        left = self.parse_term()
        while True:
            operator = self.consume( '>', '<', '==')
            if operator is None:
                break
            right = self.parse_term()
            left = BinaryOperatorNode(left, operator, right)
        return left

    def parse_term(self) -> Node:
        left = self.parse_unary()
        while True:
            operator = self.consume('*', '/')
            if operator is None:
                break
            right = self.parse_unary()
            left = BinaryOperatorNode(left, operator, right)
        return left

    def parse_unary(self) -> Node:
        if self.match('-'):
            self.advance()
            expression = self.parse_unary()
            return UnaryMinusNode(expression)
        return self.parse_power()

    def parse_power(self) -> Node:
        left = self.parse_factor()
        while True:
            operator = self.consume('^')
            if operator is None:
                break
            right = self.parse_power()
            left = BinaryOperatorNode(left, operator, right)
        return left

    def parse_factor(self) -> Node:
        current = self.current()
        if current is None:
            self.error(f"ERROR: unexpected end of expression.")
        match current:
            case NumberToken():
                number = NumberNode(current.value)
                self.advance()
                return number
            case VariableToken():
                variable = VariableNode(current.value)
                self.advance()
                return variable
            case OpeningParenthesisToken():
                self.advance()
                node = self.parse_expression()
                if self.expect(')'):
                    self.advance()
                    return node
                self.error(f"ERROR: expected closing parenthesis at position {self.current_index + 1}.")
        self.error(f"ERROR: unexpected token '{current.value}' at position {self.current_index + 1}.")

def evaluate(node: Node, memory: dict[str, Number]) -> Number | None:
    match node:
        case AssignNode():
            assign(node, memory)
            return None
        case NumberNode() | VariableNode():
            return resolve_operand(node, memory)
        case UnaryMinusNode():
            value = evaluate(node.operand, memory)
            if value is None:
                raise InvalidExpressionError(f"ERROR: expected number, got type None.")
            return unary_minus(value)
        case BinaryOperatorNode():
            left = evaluate(node.left, memory)
            right = evaluate(node.right, memory)
            if left is None or right is None:
                raise InvalidExpressionError(f"ERROR: operator '{node.operator}' requires two valid numbers, got {type(left).__name__} and {type(right).__name__}.")
            if node.operator in operations:
                return operations[node.operator](left, right)
            else:
                return comparison[node.operator](left, right)
        case IfNode():
            if not evaluate(node.condition, memory):
                if node.else_body is not None:
                    return evaluate(node.else_body, memory)
                return None
            return evaluate(node.body, memory)
        case WhileNode():
            result = None
            while evaluate(node.condition, memory):
                result = evaluate(node.body, memory)
            if not evaluate(node.condition, memory):
                if node.else_body is not None:
                    return evaluate(node.else_body, memory)
                return None
            return result
        case BlockNode():
            result = None
            for block in node.block:
                result = evaluate(block, memory)
            return result
    raise InvalidExpressionError("ERROR: unsupported AST node.")

def assign(node: AssignNode, memory: dict[str, Number]) -> None:
    value = evaluate(node.right, memory)
    if value is None:
        raise InvalidExpressionError(f"ERROR: unexpected None type.")
    memory[node.variable.value] = value
    return None

def resolve_operand(node: Node, memory: Memory) -> Number:
    match node:
        case NumberNode():
            return node.value
        case VariableNode(variable):
            if variable in memory:
                return memory[variable]
            raise InvalidExpressionError(f"ERROR: variable '{variable}' does not exist.")
        case _:
            raise InvalidExpressionError(f"ERROR: can't resolve operand for type '{type(node).__name__}'.")

if __name__ == '__main__':
    main()
