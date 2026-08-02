# expression-evaluator
a plenty of implementations of a mathematical expression evaluator.
starting from my own naive algorithm and ending with an AST-based parser.

## requirements
Python 3.11+

# prototype.
my first attempt.
works, but primitive and contains many flaws in any aspect.
example: 1 + 1 = 2
status: done.

# stack-based evaluator
a stack-based mathematical expression evaluator supporting Reverse Polish Notation (RPN) and traditional infix notation.
the evaluator uses a multi-stage processing pipeline:
input -> tokenization -> expression conversion -> evaluation -> output

## features
### Reverse Polish Notation (RPN)

example:
2 3 * 4 +
result:
10

### INFIX notation

example:
2 * 3 + 4
result:
10

switch between modes with:
INFIX
RPN

## architecture
- token-based processing.
- stack-based evaluation.
- separate lexing, parsing and evaluation stages.
- infix → RPN conversion. custom INFIX-to-RPN conversion algorithm (conceptually similar to Shunting Yard)

## variables

RPN:
x 5 =

INFIX:
x = 5

memory:
x = 5

## supported operations

binary:
- '+'
- '-'
- '*'
- '/'
- '^'

unary:
- unary '-'
- 'sqrt'
- square ('u^', RPN only)

## status: done.
the current version is feature-complete for the stack-based architecture.

# AST
builds an abstract syntax tree before evaluation
status: work in progress.
