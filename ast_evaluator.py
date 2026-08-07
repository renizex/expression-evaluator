import re
from dataclasses import dataclass
from typing import TypeAlias, NoReturn


class InvalidExpressionError(Exception):
    pass

class InvalidLexemeError(InvalidExpressionError):
    pass

Number: TypeAlias = int | float

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
    value: Node

def main() -> None:
    print("AST evaluator")
    print("currently there isn't an evaluator, so you'll just see AST instead")
    while True:
        try:
            expression = input("> ")
            tokens = lex(expression)
            parsed = parse(tokens, expression)
            print(parsed)
        except InvalidExpressionError as msg:
            print(msg)

def lex(expression: str) -> list[Token]:
    tokens = []
    matches = re.finditer(r"(\d+\.\d+|\d+)|([A-Za-z_]\w*)|([+\-*/=()^])|(\s+)|(.)", expression)
    for match in matches:
        if match.group(1):
            raw_value = match.group(1)
            number_value = float(raw_value) if '.' in raw_value else int(raw_value)
            tokens.append(NumberToken(number_value, match.start()))
        elif match.group(2):
            tokens.append(VariableToken(match.group(2), match.start()))
        elif match.group(3):
            if match.group(3) == '=':
                tokens.append(AssignToken(match.group(3), match.start()))
            elif match.group(3) == '(':
                tokens.append(OpeningParenthesisToken(match.group(3), match.start()))
            elif match.group(3) == ')':
                tokens.append(ClosingParenthesisToken(match.group(3), match.start()))
            else:
                tokens.append(BinaryOperatorToken(match.group(3), match.start()))
        elif match.group(4):
            pass
        elif match.group(5):
            raise InvalidLexemeError(f"ERROR: unknown lexeme '{match.group(5)}' at position {match.start()}.")
    return tokens

def parse(tokens: list[Token], expression: str) -> Node:
    parser = Parser(tokens, expression)
    tree = parser.parse_assignment()
    return tree

class Parser:
    def __init__(self, tokens: list[Token], expression: str) -> None:
        self.tokens = tokens
        self.expression = expression
        self.current_index = 0

    def is_valid_expression(self):
        return self.current_index < len(self.tokens)

    def current(self) -> Token | None:
        #print(self.current_index, len(self.tokens))
        if self.current_index >= len(self.tokens):
            return None
        return self.tokens[self.current_index]

    def advance(self) -> None:
        self.current_index += 1

    def error(self, message: str) -> NoReturn:
        pointer = ' ' * self.current_index + '^' if self.current_index else '^'
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

    def parse_assignment(self) -> Node:
        left = self.parse_expression()
        while True:
            operator = self.consume('=')
            if operator is None:
                break
            if not isinstance(left, VariableNode):
                self.error(f"ERROR: expected a variable, got '{left}'.")
            right = self.parse_assignment()
            left = BinaryOperatorNode(left, operator, right)
        return left

    def parse_expression(self) -> Node:
        left = self.parse_term()
        while True:
            operator = self.consume('+', '-')
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

if __name__ == '__main__':
    main()
