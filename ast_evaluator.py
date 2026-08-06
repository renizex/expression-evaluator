import re
from dataclasses import dataclass
from typing import TypeAlias

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
    value: Number | Node

def main() -> None:
    print("AST evaluator")
    print("currently there isn't an evaluator, so you'll just see AST instead")
    while True:
        try:
            expression = input("> ")
            tokens = lex(expression)
            parsed = parse(tokens)
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
            raise InvalidLexemeError(f"ERROR: unknown lexeme '{match.group(5)}' at position '{match.start()}'.")
    return tokens

def parse(tokens: list[Token]) -> Node:
    parser = Parser(tokens)
    tree = parser.parse_expression()
    return tree

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current_index = 0

    def current(self) -> Token:
        if self.current_index >= len(self.tokens):
            raise InvalidExpressionError("invalid expression")
        return self.tokens[self.current_index]

    def advance(self) -> None:
        self.current_index += 1

    def parse_expression(self) -> Node:
        left = self.parse_term()
        while self.current_index < len(self.tokens) and self.current().value in ['+', '-']:
            operator = self.current().value
            self.advance()
            right = self.parse_term()
            left = BinaryOperatorNode(left, operator, right)
        return left

    def parse_term(self) -> Node:
        left = self.parse_unary()
        while self.current_index < len(self.tokens) and self.current().value in ['*', '/']:
            operator = self.current().value
            self.advance()
            right = self.parse_unary()
            left = BinaryOperatorNode(left, operator, right)
        return left

    def parse_unary(self) -> Node:
        if self.current().value == '-':
            self.advance()
            expression = self.parse_unary()
            return UnaryMinusNode(expression)
        return self.parse_factor()

    def parse_factor(self) -> Node:
        match self.current():
            case NumberToken():
                number = NumberNode(self.current().value)
                self.advance()
                return number
            case VariableToken():
                variable = VariableNode(self.current().value)
                self.advance()
                return variable
            case OpeningParenthesisToken():
                self.advance()
                node = self.parse_expression()
                if isinstance(self.current(), ClosingParenthesisToken):
                    self.advance()
                    return node
                raise InvalidExpressionError("unmatched opening parenthesis")
        raise InvalidExpressionError("unexpected token")

if __name__ == '__main__':
    main()
